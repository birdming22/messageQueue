
import zmq  
import threading  
import time  
from random import choice  
  
class ClientTask(threading.Thread):  
    """ClientTask"""  
    def init(self):  
        threading.Thread.init (self)  
  
    def run(self):  
        context = zmq.Context()  
        socket = context.socket(zmq.XREQ)  
        identity = 'worker-%d' % (choice([0,1,2,3,4,5,6,7,8,9]))  
        socket.setsockopt(zmq.IDENTITY, identity )  
        socket.connect('tcp://localhost:5570')  
        print 'Client %s started' % (identity)  
        poll = zmq.Poller()  
        poll.register(socket, zmq.POLLIN)  
        reqs = 0  
        while True:  
            for i in xrange(5):  
                sockets = dict(poll.poll(1000))  
                if socket in sockets:  
                    if sockets[socket] == zmq.POLLIN:  
                        msg = socket.recv()  
                        print '%s: %s\n' % (identity, msg)  
                        del msg  
            reqs = reqs + 1  
            print 'Req #%d sent..' % (reqs)  
            socket.send('request #%d' % (reqs))  
  
        socket.close()  
        context.term()  
  
class ServerTask(threading.Thread):  
    """ServerTask"""  
    def init(self):  
        threading.Thread.init (self)  
  
    def run(self):  
        context = zmq.Context()  
        frontend = context.socket(zmq.XREP)  
        frontend.bind('tcp://*:5570')  
  
        backend = context.socket(zmq.XREQ)  
        backend.bind('inproc://backend')  
  
        workers = []  
        for i in xrange(5):  
            worker = ServerWorker(context)  
            worker.start()  
            workers.append(worker)  
  
        poll = zmq.Poller()  
        poll.register(frontend, zmq.POLLIN)  
        poll.register(backend,  zmq.POLLIN)  
  
        while True:  
            sockets = dict(poll.poll())  
            if frontend in sockets:  
                if sockets[frontend] == zmq.POLLIN:  
                    msg = frontend.recv()  
                    print 'Server received %s' % (msg)  
                    backend.send(msg)  
            if backend in sockets:  
                if sockets[backend] == zmq.POLLIN:  
                    msg = backend.recv()  
                    frontend.send(msg)  
  
        frontend.close()  
        backend.close()  
        context.term()  
   
class ServerWorker(threading.Thread):  
    """ServerWorker"""  
    def init(self, context):  
        threading.Thread.init (self)  
        self.context = context  
  
    def run(self):  
        worker = self.context.socket(zmq.XREQ)  
        worker.connect('inproc://backend')  
        print 'Worker started'  
        while True:  
            msg = worker.recv()  
            print 'Worker received %s' % (msg)  
            replies = choice(xrange(5))  
            for i in xrange(replies):  
                time.sleep(1/choice(range(1,10)))  
                worker.send(msg)  
            del msg  
  
        worker.close()  
  
def main():  
    """main function"""  
    print 'server task'
    server = ServerTask()  
    server.start()  
    for i in xrange(3):  
        client = ClientTask()  
        client.start()  
      
    server.join()  
      
  
if __name__ == "__main__":  
    main()  

