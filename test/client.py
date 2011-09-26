
import zmq  
import threading  
import time  
from random import choice  
import os, sys
path = os.path.split(os.getcwd())
sys.path.append(path[0])
config = __import__('config')
sys.path.pop(-1)

  
class RRC():  
    """ RRC layer
    """  
    def __init__(self):  
        self.identity = "rrc"
        print "id: %s" % self.identity

    def run(self):
        context = zmq.Context()  
        socket = context.socket(zmq.XREQ)  
        serverPort = config.DISPATCHER_PORT
        print 'serverPort: %d' % serverPort
        print 'Client %s started' % (self.identity)
        socket.setsockopt(zmq.IDENTITY, self.identity )
        socket.connect('tcp://localhost:%d' % serverPort)
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0
        while True:
            for i in xrange(5):
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    if sockets[socket] == zmq.POLLIN:
                        id, msg = socket.recv_multipart()
                        print 'recv from %s: %s\n' % (id, msg)
                        del msg
            reqs = reqs + 1
            print 'Req #%d sent..' % (reqs)
            socket.send('rlc', zmq.SNDMORE)
            socket.send('request #%d' % (reqs))

        socket.close()  
        context.term()  
   
def main():  
    client = RRC()  
    client.run()
      
  
if __name__ == "__main__":  
    main()  

