#!/usr/bin/env python3

#Written by kelseykm
##Creates TCP chatroom server with messages encrypted in TLS

import os
import socket
import sys
import threading
import ssl

HOST = ''
PORT = 1999
ADDR = (HOST, PORT)
SSL_KEY = os.path.abspath('key.pem')
SSL_CERT = os.path.abspath('cert.pem')


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(SSL_CERT, SSL_KEY)

server_s = ssl_context.wrap_socket(server, server_side=True)

print(f"[SERVER] Listening on port {PORT}...")

connections = []
nicknames = []

def broadcast(conn, mesg):
    for client in connections:
        try:
            if not client == conn:
                client.send(mesg)
        except:
            index = connections.index(client)
            connections.remove(client)

            for rem_client in connections:
                rem_client.send(f"[SERVER] {nicknames[index]} has left...\n".encode())

            nicknames.remove(nicknames[index])
            client.close()

def listener(conn):
    while True:
        data = conn.recv(1024)
        if data:
            if data.decode().upper() == 'LEAVE':
                index = connections.index(conn)
                connections.remove(conn)
                print(f"[SERVER] A client disconnected. Current active connections: {threading.activeCount()-2}")
                broadcast(conn, f"[SERVER] {nicknames[index]} has left...".encode())
                nicknames.remove(nicknames[index])
                conn.close()
                sys.exit()
            else:
                broadcast(conn, f"[{nicknames[connections.index(conn)]}] {data.decode()}".encode())

def handle(conn,addr):
    try:
        conn.send("NICK".encode())
        nick = conn.recv(1024).decode()

        connections.append(conn)
        nicknames.append(nick)

        broadcast(conn, f"[SERVER] {nick} has joined...".encode())
        if len(nicknames) > 1:
            conn.send(f"[SERVER] PEOPLE IN THE CHAT ROOM RIGHT NOW:\n\t{nicknames}\n".encode())
        else:
            conn.send("[SERVER] YOU ARE CURRENTLY THE ONLY ONE IN THE CHAT ROOM\n".encode())

        listener(conn)
    except:
        conn.close()
        sys.exit()

def accept():
    while True:
        try:
            connection, address = server_s.accept()
            print(f"[SERVER] New connection from",address)
            print(f"[SERVER] Currently connected to {threading.activeCount()} clients")

            thread = threading.Thread(target=handle, args=(connection, address))
            thread.start()
        except KeyboardInterrupt:
            server.close()
            sys.exit()
        except ssl.SSLError:
            print("[SERVER] A CLIENT TRIED TO CONNECT WITH WRONG CERTIFICATE INFORMATION. THE CONNECTION FAILED")
            pass

if __name__ == '__main__':
    accept()
