import socket
import os

CLIENT_FOLDER = 'client_files'

def send_file(client_socket, filename):
    filepath = os.path.join(CLIENT_FOLDER, filename)
    if os.path.exists(filepath):
        client_socket.send(f'upload {filename}'.encode())

        with open(filepath, 'rb') as file:
            file_data = file.read(1024)
            while file_data:
                client_socket.send(file_data)
                file_data = file.read(1024)
        client_socket.send(b'__FILE_END__')
    else:
        print("File not found.")

def receive_file(client_socket, filename):
    client_file_path = os.path.join(CLIENT_FOLDER, filename)
    with open(client_file_path, 'wb') as file:
        file_data = client_socket.recv(1024)
        while file_data and file_data != b'__FILE_END__':
            file.write(file_data)
            file_data = client_socket.recv(1024)

def main():
    if not os.path.exists(CLIENT_FOLDER):
        os.makedirs(CLIENT_FOLDER)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to server.")

    while True:
        command = input("Enter command (upload, download, list, quit): ")
        client_socket.send(command.encode())

        if command.lower() == 'quit':
            client_socket.close()
            break
        elif command.lower().startswith('upload '):
            _, filename = command.split(' ', 1)
            send_file(client_socket, filename)
        elif command.lower().startswith('download '):
            _, filename = command.split(' ', 1)
            receive_file(client_socket, filename)
        elif command.lower() == 'list':
            file_list = client_socket.recv(1024).decode()
            print("Files on the server:")
            print(file_list)
        else:
            print(client_socket.recv(1024).decode())

if __name__ == "__main__":
    main()