import socket
import os

SERVER_FOLDER = 'server_files'

def send_file(client_socket, filename):
    server_file_path = os.path.join(SERVER_FOLDER, filename)
    if os.path.exists(server_file_path):
        with open(server_file_path, 'rb') as file:
            file_data = file.read(1024)
            while file_data:
                client_socket.send(file_data)
                file_data = file.read(1024)
        client_socket.send(b'__FILE_END__')
    else:
        client_socket.send(b'__FILE_NOT_FOUND__')

def receive_file(client_socket, filename):
    server_file_path = os.path.join(SERVER_FOLDER, filename)
    with open(server_file_path, 'wb') as file:
        file_data = client_socket.recv(1024)
        while file_data and file_data != b'__FILE_END__':
            file.write(file_data)
            file_data = client_socket.recv(1024)
    if file_data == b'__FILE_END__':
        client_socket.send(b'File uploaded successfully.')
    else:
        client_socket.send(b'Error uploading file.')

def list_files(client_socket):
    files = os.listdir(SERVER_FOLDER)
    file_list = '\n'.join(files)
    client_socket.send(file_list.encode())

def main():
    if not os.path.exists(SERVER_FOLDER):
        os.makedirs(SERVER_FOLDER)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server is listening on port 12345")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            while True:
                command = client_socket.recv(1024).decode()
                if command.lower() == 'quit':
                    print(f"Closing connection with {client_address}")
                    client_socket.close()
                    break
                elif command.lower().startswith('upload '):
                    _, filename = command.split(' ', 1)
                    receive_file(client_socket, filename)
                    print(f"File {filename} uploaded by {client_address}")
                elif command.lower().startswith('download '):
                    _, filename = command.split(' ', 1)
                    send_file(client_socket, filename)
                elif command.lower() == 'list':
                    list_files(client_socket)
                else:
                    client_socket.send(b'Invalid command.')
    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main__":
    main()
