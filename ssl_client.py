from socket import *
import ssl
class my_client:
    def __init__(self, HOST, PORT):
        context = ssl.create_default_context()
        # If using self-signed certificates, you can disable verification for testing:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        sock = create_connection((HOST, PORT))
        self.ssock = context.wrap_socket(sock, server_hostname=HOST)
        # with socket.create_connection((HOST, PORT)) as sock:
        #     with context.wrap_socket(sock, server_hostname=HOST) as self.ssock:
        #         self.send_receive_message("Hello client!")

    def send_receive_message(self, msg):
        print(f"sending message => {msg}")
        self.ssock.sendall(msg.encode())
        answer = self.ssock.recv(1024).decode()
        print(answer)
        self.ssock.close()



if __name__ == "__main__":
    client = my_client("127.0.0.1", 12345)
    request = str(input(""))
    client.send_receive_message(request)