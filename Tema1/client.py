import socket
import time
import argparse
import sys


def send_data_TCP_streaming(localhost, port, size, num, buffer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.connect(server_address)

    start_time = time.time()
    total_bytes_sent = 0
    message_size = round(size / num)

    print("Message size : " + str(message_size) + "   Buffer : " + str(buffer))

    sent = sock.sendall(bytes(str(message_size), encoding='utf-8'))
    sent = sock.sendall(bytes(str(buffer), encoding='utf-8'))

    for i in range(num):
        message = b'0' * message_size

        bytes_sent = 0
        while bytes_sent < message_size:
            chunk = message[bytes_sent:bytes_sent + buffer]
            data = sock.sendall(chunk)
            bytes_sent += len(chunk)

        total_bytes_sent += len(message)

        data = sock.recv(buffer)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Num?r de mesaje trimise: {num}")
    print(f"Num?r de bytes trimi?i: {total_bytes_sent}")

    sock.close()


def send_data_TCP_stop_and_wait(localhost, port, size, num, buffer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.connect(server_address)

    start_time = time.time()
    total_bytes_sent = 0
    message_size = round(size / num)

    print("Message size : " + str(message_size) + "   Buffer : " + str(buffer))

    sent = sock.sendall(bytes(str(message_size), encoding='utf-8'))
    sent = sock.sendall(bytes(str(buffer), encoding='utf-8'))

    for i in range(num):
        message = b'0' * message_size

        bytes_sent = 0
        while bytes_sent < message_size:
            chunk = message[bytes_sent:bytes_sent + buffer]
            data = sock.sendall(chunk)
            bytes_sent += len(chunk)

        while True:
            data = sock.recv(buffer)

            if (data.decode() == "Serverul a primit mesajul!"):
                total_bytes_sent += len(message)

                sent = sock.sendall(b"Clientul a primit mesajul de la server!")
                break

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Num?r de mesaje trimise: {num}")
    print(f"Num?r de bytes trimi?i: {total_bytes_sent}")

    sock.close()


def send_data_UDP_streaming(localhost, port, size, num, buffer):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)

    start_time = time.time()
    total_bytes_sent = 0
    message_size = round(size / num)

    print("Message size : " + str(message_size) + "   Buffer : " + str(buffer))

    sent = sock.sendto(bytes(str(message_size), encoding='utf-8'), server_address)
    sent = sock.sendto(bytes(str(buffer), encoding='utf-8'), server_address)

    for i in range(num):
        message = b'0' * message_size

        bytes_sent = 0
        while bytes_sent < message_size:
            chunk = message[bytes_sent:bytes_sent + buffer]
            data = sock.sendto(chunk, server_address)
            bytes_sent += len(chunk)

        total_bytes_sent += len(message)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Num?r de mesaje trimise: {num}")
    print(f"Num?r de bytes trimi?i: {total_bytes_sent}")

    sock.close()


def send_data_UDP_stop_and_wait(localhost, port, size, num, buffer):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)

    start_time = time.time()
    total_bytes_sent = 0
    message_size = round(size / num)

    print("Message size : " + str(message_size) + "   Buffer : " + str(buffer))

    sent = sock.sendto(bytes(str(message_size), encoding='utf-8'), server_address)
    sent = sock.sendto(bytes(str(buffer), encoding='utf-8'), server_address)

    for i in range(num):
        message = b'0' * message_size

        bytes_sent = 0
        while bytes_sent < message_size:
            chunk = message[bytes_sent:bytes_sent + buffer]
            data = sock.sendto(chunk, server_address)
            bytes_sent += len(chunk)

        while True:
            data, server = sock.recvfrom(buffer)

            if (data.decode() == "Serverul a primit mesajul!"):
                total_bytes_sent += len(message)
                sent = sock.sendto(b"Clientul a primit mesajul de la server!", server)
                break

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Num?r de mesaje trimise: {num}")
    print(f"Num?r de bytes trimi?i: {total_bytes_sent}")

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
parser.add_argument('-size', '--size_message', type=str, choices=[
      '10485760', '52428800', '104857600', '524288000', '1073741824'], required=True, help='dimensiunea datelor trimise in bytes')
parser.add_argument('-nr', '--number_messages', type=str, choices=[
      '5', '10', '100', '500', '1000'], required=True, help='numarul de mesaje trimise')
parser.add_argument('-bf', '--buffer_size', type=str, choices=[
      '15500', '32500', '65000'], required=True, help='dimensiunea buffer-ului')


args = parser.parse_args()


if (args.connection.upper() == "TCP"):
    if (args.transfer_mode.lower() == "streaming"):
        send_data_TCP_streaming(args.ip_address, args.port, int(args.size_message), int(args.number_messages), int(args.buffer_size))
    elif (args.transfer_mode.lower() == "stop-and-wait"):
        send_data_TCP_stop_and_wait(args.ip_address, args.port, int(args.size_message), int(args.number_messages), int(args.buffer_size))
    else:
        print("Mecanismul specificat nu este suportat!")
        exit(0)
elif (args.connection.upper() == "UDP"):
    if (args.transfer_mode.lower() == "streaming"):
        send_data_UDP_streaming(args.ip_address, args.port, int(args.size_message), int(args.number_messages), int(args.buffer_size))
    elif (args.transfer_mode.lower() == "stop-and-wait"):
        send_data_UDP_stop_and_wait(args.ip_address, args.port, int(args.size_message), int(args.number_messages), int(args.buffer_size))
    else:
        print("Mecanismul specificat nu este suportat!")
        exit(0)
else:
    print("Protocolul specificat nu este suportat!")
    exit(0)