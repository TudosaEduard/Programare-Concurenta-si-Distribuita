import socket
import argparse
import sys
import time


def start_server_TCP_streaming(localhost, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    sock.listen(1)

    connection, client_address = sock.accept()

    # take size and buffer from the client
    message_size = int.from_bytes(connection.recv(8), byteorder='big')
    message_buffer = int.from_bytes(connection.recv(8), byteorder='big')

    print("Message size : " + str(message_size) + "   Buffer : " + str(message_buffer))

    message = b''
    bytes_read = 0
    messages_read = 0

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000000)

    while True:
        chunk = connection.recv(message_buffer)
        if not chunk:
            # if there is no more data to receive, we exit the loop
            break 
        message += chunk
        bytes_read += len(chunk)
        messages_read += 1

        if(bytes_read == message_size):
            break


    print(f"Protocol folosit: {args.connection.upper() }")
    print(f"Numar de mesaje citite: {messages_read}")
    print(f"Numar de bytes cititi: {bytes_read}")
    print(f"Numar de bytes pierduti: {message_size - bytes_read}")

    connection.close()
    sock.close()


def start_server_TCP_stop_and_wait(localhost, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    sock.listen(1)

    connection, client_address = sock.accept()

    # take size and buffer from the client
    message_size = int.from_bytes(connection.recv(8), byteorder='big')
    message_buffer = int.from_bytes(connection.recv(8), byteorder='big')

    print("Message size : " + str(message_size) + "   Buffer : " + str(message_buffer))

    message = b''
    bytes_read = 0
    messages_read = 0

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000000)

    while True:
        chunk = connection.recv(message_buffer)
        if not chunk:
            # if there is no more data to receive, we exit the loop
            break
        
        message += chunk
        bytes_read += len(chunk)
        messages_read += 1

        response = b'ACK'
        data = connection.send(response)

        if(bytes_read == message_size):
            break
    


    print(f"Protocol folosit: {args.connection.upper() }")
    print(f"Numar de mesaje citite: {messages_read}")
    print(f"Numar de bytes cititi: {bytes_read}")
    print(f"Numar de bytes pierduti: {message_size - bytes_read}")

    connection.close()
    sock.close()


def start_server_UDP_streaming(localhost, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    message_size, client_address = sock.recvfrom(8)
    message_buffer, client_address = sock.recvfrom(8)

    message_size = int.from_bytes(message_size, byteorder='big')
    message_buffer = int.from_bytes(message_buffer, byteorder='big')

    print("Message size : " + str(message_size) + "   Buffer : " + str(message_buffer))

    message = b''
    bytes_read = 0
    messages_read = 0

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000000)

    while True:
        chunk, client_address = sock.recvfrom(message_buffer)
        if not chunk:
            # if there is no more data to receive, we exit the loop
            break
        
        message += chunk
        bytes_read += len(chunk)
        messages_read += 1

        if(bytes_read == message_size):
            break


    print(f"Protocol folosit: {args.connection.upper() }")
    print(f"Numar de mesaje citite: {messages_read}")
    print(f"Numar de bytes cititi: {bytes_read}")
    print(f"Numar de bytes pierduti: {message_size - bytes_read}")

    sock.close()


def start_server_UDP_stop_and_wait(localhost, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    message_size, client_address = sock.recvfrom(8)
    message_buffer, client_address = sock.recvfrom(8)

    message_size = int.from_bytes(message_size, byteorder='big')
    message_buffer = int.from_bytes(message_buffer, byteorder='big')

    print("Message size : " + str(message_size) + "   Buffer : " + str(message_buffer))

    message = b''
    bytes_read = 0
    messages_read = 0

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000000)

    while True:
        chunk, client_address = sock.recvfrom(message_buffer)
        if not chunk:
            # if there is no more data to receive, we exit the loop
            break
        
        message += chunk
        bytes_read += len(chunk)
        messages_read += 1

        response = b'ACK'
        data = sock.sendto(response, client_address)

        if(bytes_read == message_size):
            break

    print(f"Protocol folosit: {args.connection.upper() }")
    print(f"Numar de mesaje citite: {messages_read}")
    print(f"Numar de bytes cititi: {bytes_read}")
    print(f"Numar de bytes pierduti: {message_size - bytes_read}")

    sock.close()


parser = argparse.ArgumentParser(description='TCP/UDP Server')
parser.add_argument('-c', '--connection', type=str,
                    choices=['TCP', 'UDP'], required=True, help='tipul de conexiune: TCP sau UDP')
parser.add_argument('-ip', '--ip_address', type=str,
                    required=True, help='adresa IP a serverului')
parser.add_argument('-p', '--port', type=int, required=True,
                     help='portul de ascultare al serverului')
parser.add_argument('-t', '--transfer_mode', type=str, choices=[
      'streaming', 'stop-and-wait'], required=True, help='modul de transfer: streaming sau stop-and-wait')

args = parser.parse_args()

if (args.connection.upper() == "TCP"):
    if (args.transfer_mode.lower() == "streaming"):
            start_server_TCP_streaming(args.ip_address, args.port)
    elif (args.transfer_mode.lower() == "stop-and-wait"):
            start_server_TCP_stop_and_wait(args.ip_address, args.port)
    else:
        print("Mecanismul specificat nu este suportat!")
        exit(0)
elif (args.connection.upper() == "UDP"):
    if (args.transfer_mode.lower() == "streaming"):
            start_server_UDP_streaming(args.ip_address, args.port)
    elif (args.transfer_mode.lower() == "stop-and-wait"):
            start_server_UDP_stop_and_wait(args.ip_address, args.port)
    else:
            print("Mecanismul specificat nu este suportat!")
            exit(0)
else:
    print("Protocolul specificat nu este suportat!")
    exit(0)