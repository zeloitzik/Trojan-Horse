from socket import *
import ssl
import os
from dotenv import load_dotenv
import mysql.connector
from sql_setup import table


class my_server:
    def __init__(self, PORT, HOST):
        # Create a standard TCP socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
      
        
    def server_listen(self):
        self.server_socket.listen(5)
        print(f"Server listening...")

        # Wrap the socket with SSL
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='server.crt', keyfile='server.key')

        try:
            with context.wrap_socket(self.server_socket, server_side=True) as ssock:
                while True:
                    conn, addr = ssock.accept()
                    print(f"Connection from {addr}")
                    data = conn.recv(1024)
                    print(f"Received: {data.decode()}")
                    #conn.sendall(b"Hello from the server!")
                    self.handle_random_key(conn)
                    conn.close()
        except Exception as e:
            print(f"Error: {e}")
            
    def receive_msg(self, client):
        self.message = client.recv(1024).decode()

    def generateRandomKey(self):
        return os.urandom(16)
    
    def handle_random_key(self, client):
        self.key = self.generateRandomKey()
        print(f"Generated key: {self.key.hex()}")
        self.table = table()
        self.table.Insert_Client(client.getpeername()[0], self.key.hex())
        self.table.Print_table()
        client.sendall(self.key)

    def print_table(self):
        self.table.Print_table()  
    def reset_all(self):
        self.table.reset_all()
        print("All data has been reset in the database.")  

def main():
    server = my_server(12345, "127.0.0.1")
    server.server_listen()
main()   
