import socket
import argparse
import sys
import time


def start_server_TCP_streaming(localhost, port):
    total_bytes_read = 0
    total_messages_read = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    sock.listen(1)

    # Astept conexiune de la un client
    connection, client_address = sock.accept()

    # S-a stabilit conexiunea cu clientul

    message_size = int(connection.recv(65535))
    buffer = int(connection.recv(65535))

    print("Message size : " + str(message_size) + "   Buffer : " + str(buffer))

    max_idle_time = 5
    connection.settimeout(5)

    while True:
        message = b''
        bytes_read = 0

        try:
            while bytes_read < message_size:
                chunk = connection.recv(buffer)
                if not chunk:
                    # Daca nu mai sunt date de primit, iesim din bucla
                    break
                message += chunk
                bytes_read += len(chunk)

            if not message:
                # Daca nu s-a primit niciun mesaj, ie?im din bucla
                break
            else:
                total_bytes_read += len(message)
                total_messages_read += 1
                connection.sendall(b"Serverul a primit mesajul!")

            # Reseteaza timpul
            last_message_time = time.time()

        except socket.timeout:
            # Daca a expirat timeout-ul, iesim din bucla
            break

        # Verifica daca a trecut suficient timp de la primirea ultimului mesaj
        if time.time() - last_message_time > max_idle_time:
            break

    print(f"Protocol folosit: {args.connection.upper() }")
    print(f"Num?r de mesaje citite: {total_messages_read}")
    print(f"Num?r de bytes citi?i: {total_bytes_read}")

    connection.close()
    sock.close()


def start_server_TCP_stop_and_wait(localhost, port):
    total_bytes_read = 0
    total_messages_read = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    sock.listen(1)

    # Astept conexiune de la un client
    connection, client_address = sock.accept()

    # S-a stabilit conexiunea cu clientul

    message_size = int(connection.recv(65535))
    buffer = int(connection.recv(65535))

    print("Message size : " + str(message_size) + "   Buffer : " + str(buffer))

    max_idle_time = 5
    connection.settimeout(5)

    while True:
        message = b''
        bytes_read = 0

        try:
            while bytes_read < message_size:
                chunk = connection.recv(buffer)
                if not chunk:
                    # Daca nu mai sunt date de primit, iesim din bucla
                    break
                message += chunk
                bytes_read += len(chunk)

            if not message:
                # Daca nu s-a primit niciun mesaj, iesim din bucla
                break
            else:
                total_bytes_read += len(message)
                while True:
                    connection.sendall(b"Serverul a primit mesajul!")
                    data = connection.recv(buffer)

                    if (data.decode() == "Clientul a primit mesajul de la server!"):
                        total_messages_read += 1
                        break
            
            # Reseteaza timpul
            last_message_time = time.time()

        except socket.timeout:
            # Daca a expirat timeout-ul, iesim din bucla
            break

        # Verifica daca a trecut suficient timp de la primirea ultimului mesaj
        if time.time() - last_message_time > max_idle_time:
            break

    print(f"Protocol folosit: {args.connection.upper()}")
    print(f"Num?r de mesaje citite: {total_messages_read}")
    print(f"Num?r de bytes citi?i: {total_bytes_read}")

    connection.close()
    sock.close()


def start_server_UDP_streaming(localhost, port):
    total_bytes_read = 0
    total_messages_read = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    # Astept conexiune de la un client
    message_size, client_address = sock.recvfrom(65507)
    buffer, client_address = sock.recvfrom(65507)

    message_size = int(message_size)
    buffer = int(buffer)

    print("Message size : " + str(message_size) + "   Buffer : " + str(buffer))

    while True:
        max_idle_time = 10
        sock.settimeout(10)

        message = b''
        bytes_read = 0

        while bytes_read < message_size:
            try:
                chunk, client_address = sock.recvfrom(buffer)
                if not chunk:
                    # Daca nu mai sunt date de primit, iesim din bucla
                    break
                message += chunk
                bytes_read += len(chunk)

                # Reseteaza timpul
                last_message_time = time.time()
            except socket.timeout:
                # Daca a expirat timeout-ul, iesim din bucla
                break

            # Verifica daca a trecut suficient timp de la primirea ultimului mesaj
            if time.time() - last_message_time > max_idle_time:
                break

        if not message:
            # Daca nu s-a primit niciun mesaj, iesim din bucla
            break
        else:
            total_bytes_read += len(message)
            total_messages_read += 1


    print(f"Protocol folosit: {args.connection.upper()}")
    print(f"Num?r de mesaje citite: {total_messages_read}")
    print(f"Num?r de bytes citi?i: {total_bytes_read}")

    sock.close()


def start_server_UDP_stop_and_wait(localhost, port):
    total_bytes_read = 0
    total_messages_read = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)
    sock.bind(server_address)

    # Astept conexiune de la un client

    message_size, client_address = sock.recvfrom(65507)
    buffer, client_address = sock.recvfrom(65507)

    message_size = int(message_size)
    buffer = int(buffer)

    print("Message size : " + str(message_size) + "   Buffer : " + str(buffer))

    while True:
        max_idle_time = 10
        sock.settimeout(10)

        message = b''
        bytes_read = 0

        while bytes_read < message_size:
            try:
                chunk, client_address = sock.recvfrom(buffer)
                if not chunk:
                    # Daca nu mai sunt date de primit, iesim din bucla
                    break
                message += chunk
                bytes_read += len(chunk)

                # Reseteaza timpul
                last_message_time = time.time()

            except socket.timeout:
                # Daca a expirat timeout-ul, iesim din bucla
                break

            # Verifica daca a trecut suficient timp de la primirea ultimului mesaj
            if time.time() - last_message_time > max_idle_time:
                break

        if not message:
            # Daca nu s-a primit niciun mesaj, iesim din bucla
            break
        else:
            total_bytes_read += len(message)
            while True:
                sock.sendto(b"Serverul a primit mesajul!", client_address)
                data, client_address = sock.recvfrom(buffer)

                if (data.decode() == "Clientul a primit mesajul de la server!"):
                    total_messages_read += 1
                    break


    print(f"Protocol folosit: {args.connection.upper()}")
    print(f"Num?r de mesaje citite: {total_messages_read}")
    print(f"Num?r de bytes citi?i: {total_bytes_read}")

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