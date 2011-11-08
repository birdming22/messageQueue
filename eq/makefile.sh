#bin/sh
gcc server.c -o server -lzmq
gcc rserver.c -o rserver -lzmq
gcc broker.c -o broker -lzmq
gcc rclient.c -o rclient -lzmq
gcc client.c -o client -lzmq
gcc client2.c -o client2 -lzmq
gcc async.c -o async -lzmq -lczmq
