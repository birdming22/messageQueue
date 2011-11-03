//
//  Hello World client
//  Connects REQ socket to tcp://localhost:5555
//  Sends "Hello" to server, expects "World" back
//
#include <zmq.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>


static char * s_recv (void *socket) {
    zmq_msg_t message;
    zmq_msg_init (&message);
    zmq_recv (socket, &message, 0);
    int size = zmq_msg_size (&message);
    char *string = malloc (size + 1);
    memcpy (string, zmq_msg_data (&message), size);
    zmq_msg_close (&message);
    string [size] = 0;
    return (string);
}

int main (void)
{
    void *context = zmq_init (1);
    //  Socket to talk to server
    printf ("Connecting to hello world server…\n");
    void *requester = zmq_socket (context, ZMQ_XREQ);
    zmq_connect (requester, "tcp://localhost:5555");

    int request_nbr;
    request_nbr=1;
    // fixme
    char* client_id = "1";
    char *out;
    int more;
    size_t more_size = sizeof more;


    zmq_msg_t id;
    zmq_msg_t request;
    zmq_msg_init_size (&id, 1);
    zmq_msg_init_size (&request, 5);

    memcpy (zmq_msg_data (&id), client_id, 1);
    zmq_send (requester, &id, ZMQ_SNDMORE);

    memcpy (zmq_msg_data (&request), "Hello", 5);
    zmq_send (requester, &request, 0);

    zmq_msg_close (&id);
    zmq_msg_close (&request);

    printf("send Hello to server\n");

    do {
        zmq_msg_t reply;
        zmq_msg_init (&reply);

        printf ("start Received msg: \n");

        zmq_recv (requester, &reply, 0);
        out = (char*)zmq_msg_data(&reply);
        printf ("Received msg: %s\n", out);

        zmq_getsockopt (requester, ZMQ_RCVMORE, &more, &more_size);

        zmq_msg_close (&reply);

    } while (more);

    zmq_close (requester);
    zmq_term (context);
    return 0;
}

