import socket
import time
import argparse
import sys

limbaje = ["Java", "Python", "C", "C++", "C#", "PHP", "Haskell", "Javascript"]


def send_data_TCP_streaming(localhost, port, num_messages):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.connect(server_address)

    start_time = time.time()
    total_bytes_sent = 0
    lang = 0

    for i in range(num_messages):
        message = "Astazi voi invata limbajul " + limbaje[lang] + "."
        message = bytes(message, encoding='utf-8')
        total_bytes_sent += len(message)
        sent = sock.sendall(message)

        data = sock.recv(65535)
        print(f"Clientul a primit mesajul de la server!")

        lang += 1
        if (lang > 7):
            lang = 0

    sent = sock.sendall(b"Conexiune oprita!")

    data = sock.recv(65535)
    print(data.decode())

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Număr de mesaje trimise: {num_messages}")
    print(f"Număr de bytes trimiși: {total_bytes_sent}")

    sock.close()


def send_data_TCP_stop_and_wait(localhost, port, num_messages):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.connect(server_address)

    start_time = time.time()
    total_bytes_sent = 0
    lang = 0

    for i in range(num_messages):
        message = "Astazi voi invata limbajul " + limbaje[lang] + "."
        message = bytes(message, encoding='utf-8')
        sent = sock.sendall(message)

        while True:
            data = sock.recv(65535)

            if (data.decode() == "Serverul a primit mesajul!"):
                print(f"Clientul a primit mesajul de la server!")
                total_bytes_sent += len(message)

                sent = sock.sendall(b"Clientul a primit mesajul de la server!")
                break

        lang += 1
        if (lang > 7):
            lang = 0

    sent = sock.sendall(b"Conexiune oprita!")

    data = sock.recv(65535)
    print(data.decode())

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Număr de mesaje trimise: {num_messages}")
    print(f"Număr de bytes trimiși: {total_bytes_sent}")

    sock.close()


def send_data_UDP_streaming(localhost, port, num_messages):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)

    start_time = time.time()
    total_bytes_sent = 0
    lang = 0

    for i in range(num_messages):
        message = "Astazi voi invata limbajul " + limbaje[lang] + "."
        message = bytes(message, encoding='utf-8')

        total_bytes_sent += len(message)
        sent = sock.sendto(message, server_address)

        data, server = sock.recvfrom(65507)
        print(f"Clientul a primit mesajul de la server!")

        lang += 1
        if (lang > 7):
            lang = 0

    sent = sock.sendto(b"Conexiune oprita!", server_address)

    data, server = sock.recvfrom(65507)
    print(data.decode())

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Număr de mesaje trimise: {num_messages}")
    print(f"Număr de bytes trimiși: {total_bytes_sent}")

    sock.close()


def send_data_UDP_stop_and_wait(localhost, port, num_messages):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)

    start_time = time.time()
    total_bytes_sent = 0
    lang = 0

    for i in range(num_messages):
        message = "Astazi voi invata limbajul " + limbaje[lang] + "."
        message = bytes(message, encoding='utf-8')

        total_bytes_sent += len(message)
        sent = sock.sendto(message, server_address)

        while True:

            data, server = sock.recvfrom(65507)
            print(f"Clientul a primit mesajul de la server!")

            if (data.decode() == "Serverul a primit mesajul!"):
                sent = sock.sendto(
                    b"Clientul a primit mesajul de la server!", server_address)
                break

        lang += 1
        if (lang > 7):
            lang = 0

    sent = sock.sendto(b"Conexiune oprita!", server_address)

    data, server = sock.recvfrom(65507)
    print(data.decode())

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Număr de mesaje trimise: {num_messages}")
    print(f"Număr de bytes trimiși: {total_bytes_sent}")

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
        send_data_TCP_streaming(args.ip_address, args.port, 100000)
    elif (args.transfer_mode.lower() == "stop-and-wait"):
        send_data_TCP_stop_and_wait(args.ip_address, args.port, 100000)
    else:
        print("Mecanismul specificat nu este suportat!")
        exit(0)
elif (args.connection.upper() == "UDP"):
    if (args.transfer_mode.lower() == "streaming"):
        send_data_UDP_streaming(args.ip_address, args.port, 100000)
    elif (args.transfer_mode.lower() == "stop-and-wait"):
        send_data_UDP_stop_and_wait(args.ip_address, args.port, 100000)
    else:
        print("Mecanismul specificat nu este suportat!")
        exit(0)
else:
    print("Protocolul specificat nu este suportat!")
    exit(0)
