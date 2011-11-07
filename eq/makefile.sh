#bin/sh
gcc server.c -o server -lzmq
gcc client.c -o client -lzmq
gcc client2.c -o client2 -lzmq
