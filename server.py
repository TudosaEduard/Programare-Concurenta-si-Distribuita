import socket
import argparse
import sys


def start_server_TCP_streaming(localhost, port):
    total_bytes_read = 0
    total_messages_read = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    sock.listen(1)

    print(
        f"Aștept conexiune de la un client pe {server_address[0]}:{server_address[1]}")
    connection, client_address = sock.accept()

    print(
        f"S-a stabilit conexiunea cu clientul {client_address[0]}:{client_address[1]}")

    while True:
        data = connection.recv(65535)

        if data.decode() == "Conexiune oprita!":
            print("Conexiune oprita!")
            connection.sendall(b"Serverul a fost oprit!")
            break

        total_bytes_read += len(data)
        total_messages_read += 1

        connection.sendall(b"Serverul a primit mesajul!")

        print(f"Serverul a primit mesajul: {data.decode()}")

    print(f"Protocol folosit: {args.connection.upper() }")
    print(f"Număr de mesaje citite: {total_messages_read}")
    print(f"Număr de bytes citiți: {total_bytes_read}")

    connection.close()
    sock.close()


def start_server_TCP_stop_and_wait(localhost, port):
    total_bytes_read = 0
    total_messages_read = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    sock.listen(1)

    print(
        f"Aștept conexiune de la un client pe {server_address[0]}:{server_address[1]}")
    connection, client_address = sock.accept()

    print(
        f"S-a stabilit conexiunea cu clientul {client_address[0]}:{client_address[1]}")

    while True:
        data = connection.recv(65535)

        if data.decode() == "Conexiune oprita!":
            print("Conexiune oprita!")
            connection.sendall(b"Serverul a fost oprit!")
            break

        total_bytes_read += len(data)

        while True:
            connection.sendall(b"Serverul a primit mesajul!")
            data = connection.recv(65535)

            if (data.decode() == "Clientul a primit mesajul de la server!"):
                total_messages_read += 1
                break

        print(f"Serverul a primit mesajul: {data.decode()}")

    print(f"Protocol folosit: {args.connection.upper()}")
    print(f"Număr de mesaje citite: {total_messages_read}")
    print(f"Număr de bytes citiți: {total_bytes_read}")

    connection.close()
    sock.close()


def start_server_UDP_streaming(localhost, port):
    total_bytes_read = 0
    total_messages_read = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    print(
        f"Aștept conexiune de la un client pe {server_address[0]}:{server_address[1]}")

    while True:
        data, client_address = sock.recvfrom(65507)

        if data.decode() == "Conexiune oprita!":
            print("Conexiune oprita!")
            sock.sendto(b"Serverul a fost oprit!", client_address)
            break

        total_bytes_read += len(data)
        total_messages_read += 1

        sock.sendto(b"Serverul a primit mesajul!", client_address)

        print(f"Serverul a primit mesajul: {data.decode()}")

    print(f"Protocol folosit: {args.connection.upper()}")
    print(f"Număr de mesaje citite: {total_messages_read}")
    print(f"Număr de bytes citiți: {total_bytes_read}")

    sock.close()


def start_server_UDP_stop_and_wait(localhost, port):
    total_bytes_read = 0
    total_messages_read = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    print(
        f"Aștept conexiune de la un client pe {server_address[0]}:{server_address[1]}")

    while True:
        data, client_address = sock.recvfrom(65507)

        if data.decode() == "Conexiune oprita!":
            print("Conexiune oprita!")
            sock.sendto(b"Serverul a fost oprit!", client_address)
            break

        total_bytes_read += len(data)
        total_messages_read += 1

        while True:

            sock.sendto(b"Serverul a primit mesajul!", client_address)
            data, client_address = sock.recvfrom(65507)
            if (data.decode() == "Clientul a primit mesajul de la server!"):
                break

        print(f"Serverul a primit mesajul: {data.decode()}")

    print(f"Protocol folosit: {args.connection.upper()}")
    print(f"Număr de mesaje citite: {total_messages_read}")
    print(f"Număr de bytes citiți: {total_bytes_read}")

    sock.close()


parser = argparse.ArgumentParser(description='TCP Server')
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
