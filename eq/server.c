//
//  Hello World server
//  Binds REP socket to tcp://*:5555
//  Expects "Hello" from client, replies with "World"
//
#include <zmq.h>
#include <stdio.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>

static int
s_send (void *socket, char *string) {
    int rc;
    zmq_msg_t message;
    zmq_msg_init_size (&message, strlen (string));
    memcpy (zmq_msg_data (&message), string, strlen (string));
    rc = zmq_send (socket, &message, 0);
    assert (!rc);
    zmq_msg_close (&message);
    return (rc);
}

zmq_msg_t mapping[1000];

zmq_msg_t * get_zmq_id(int client_id) {
    if(client_id > 0)
        return &(mapping[client_id]);
}

int main (void)
{
    void *context = zmq_init (1);

    //  Socket to talk to clients
    void *responder = zmq_socket (context, ZMQ_ROUTER);
    zmq_bind (responder, "tcp://*:5555");
                //  Wait for next request from client


    char* out;

    while (1) {

        zmq_msg_t zmq_id;
        zmq_msg_t client_id;
        zmq_msg_t request;

        zmq_msg_init (&zmq_id);
        zmq_msg_init (&client_id);
        zmq_msg_init (&request);

        zmq_recv (responder, &zmq_id, 0);
        out = (char*)zmq_msg_data(&zmq_id);
        printf ("Received %s\n", out);

        zmq_recv (responder, &client_id, 0);
        out = (char*)zmq_msg_data(&client_id);
        printf ("Received %s\n", out);

        // fixme
        int int_client_id = atoi(out);
        mapping[int_client_id] = zmq_id;

        zmq_recv (responder, &request, 0);
        out = (char*)zmq_msg_data(&request);
        printf ("Received %s\n", out);


        //  Do some 'work'
        sleep (1);

        printf("send to client id: %d\n", int_client_id);

        zmq_send (responder, get_zmq_id(int_client_id), ZMQ_SNDMORE);
        zmq_msg_t reply;
        zmq_msg_init_size (&reply, 5);
        memcpy (zmq_msg_data (&reply), "World", 5);

        zmq_send (responder, &reply, 0);

        zmq_msg_close (&reply);

        printf("Send data to client...\n");

        zmq_msg_close (&request);
        zmq_msg_close (&client_id);
        zmq_msg_close (&zmq_id);
    }

    //  We never get here but if we did, this would be how we end
    zmq_close (responder);
    zmq_term (context);

    return 0;
}

