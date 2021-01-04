#!/usr/bin/env python3

#Written by kelseykm
##Creates TCP chatroom client with messages encrypted in TLS

import os
import socket
import sys
import threading
import ssl

HOST = '127.0.0.1'
PORT = 1999
ADDR = (HOST, PORT)
SSL_CERT = os.path.abspath('cert.pem')


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(SSL_CERT)

client_s = ssl_context.wrap_socket(client, server_hostname='ALLANON')
try:
    client_s.connect(ADDR)
except ssl.SSLCertVerificationError:
    print("SERVER CERTIFICATE VERIFICATION FAILED")
    sys.exit()

NICK = input("PLEASE ENTER NICK: ")
print("IF YOU WISH TO LEAVE THE CHAT ROOM PLEASE TYPE 'LEAVE'\n")

def receiver():
    while True:
        try:
            data_recv = client_s.recv(1024)
            if data_recv.decode() == 'NICK':
                client_s.send(NICK.encode())
            else:
                print(data_recv.decode())
        except:
            sys.exit()

def sender():
    while True:
        data_send = input()
        if data_send:
            try:
                if data_send.upper() == 'LEAVE':
                    client_s.send(data_send.encode())
                    client_s.close()
                    sys.exit()
                else:
                    client_s.send(data_send.encode())
            except:
                client_s.close()
                sys.exit()

if __name__ == '__main__':
    thread_1 = threading.Thread(target=receiver)
    thread_2 = threading.Thread(target=sender)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    print("YOU HAVE LEFT THE CHAT ROOM...")
