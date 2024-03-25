import socket
import time

def send_message(message):
    host = '127.0.0.1'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode('utf-8'))

if __name__ == "__main__":
    # Example: Sending messages every 2 seconds
    while True:
        message = input("Enter message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        send_message(message)
        time.sleep(2)