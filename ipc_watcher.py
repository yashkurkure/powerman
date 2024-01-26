import socket

def start_listener():
    host = '127.0.0.1'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Listening for messages on {host}:{port}")
        conn, addr = s.accept()

        with conn:
            print(f"Connected by: {addr}")

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received message: {data.decode('utf-8')}")

if __name__ == "__main__":
    start_listener()