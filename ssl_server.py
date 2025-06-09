from socket import *
import ssl
import os
from dotenv import load_dotenv
import mysql.connector
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
                    conn.sendall(b"Hello from the server!")
                    conn.close()
        except Exception as e:
            print(f"Error: {e}")
            
    def receive_msg(self, client):
        self.message = client.recv(1024).decode()

    def generateRandomKey(self):
        return os.urandom(32)

    def SetUp_SQL(self):
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        database = "database_key"
        mydb = mysql.connector.connect(
                host="127.0.0.1",
                user=db_user,
                password=db_password,
                database=database
        )

        cursor = mydb.cursor()
        cursor.execute("CREATE TABLE keys (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) key key STRING(32))")

def main():
    server = my_server(12345, "127.0.0.1")
    server.server_listen()
main()   
