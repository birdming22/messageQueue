
import zmq  
import time  
from random import choice  
import os, sys
path = os.path.split(os.getcwd())
sys.path.append(path[0])
config = __import__('config')
sys.path.pop(-1)

  
class Dispatcher():  
    """ Dispatcher: dispatch message
    """  
    def __init__(self):  
        pass

    def run(self):
        context = zmq.Context()  
        frontend = context.socket(zmq.ROUTER)  
        serverPort = config.DISPATCHER_PORT
        print 'serverPort: %d' % serverPort
        frontend.bind('tcp://*:%d' % serverPort)  
  
        #backend = context.socket(zmq.XREQ)  
        #backend.bind('inproc://backend')  
  
        poll = zmq.Poller()  
        poll.register(frontend, zmq.POLLIN)  
        #poll.register(backend,  zmq.POLLIN)  
  
        while True:  
            sockets = dict(poll.poll())  
            if frontend in sockets:  
                if sockets[frontend] == zmq.POLLIN:  
                    src, dst, msg = frontend.recv_multipart()  
                    print 'Server received %s from %s to %s' % (msg, src, dst)  
                    #rsp = self.msgHandler(msg)
                    frontend.send("rrc", zmq.SNDMORE)
                    frontend.send("rlc", zmq.SNDMORE)
                    frontend.send(msg)
                    #backend.send(msg)  
            """
            if backend in sockets:  
                if sockets[backend] == zmq.POLLIN:  
                    msg = backend.recv()  
                    frontend.send(msg)  
            """
  
        frontend.close()  
        #backend.close()  
        context.term()  
   
def main():  
    dispatcher = Dispatcher()  
    dispatcher.run()
      
  
if __name__ == "__main__":  
    main()  

