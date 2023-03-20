import socket
import time
import argparse
import sys


def send_data_TCP_streaming(localhost, port, message_size, message_buffer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.connect(server_address)

    start_time = time.time()

    print("Message size : " + str(message_size) + "   Buffer : " + str(message_buffer))

    # send the message size and buffer to the server
    sent = sock.send(message_size.to_bytes(8, byteorder='big'))
    sent = sock.send(message_buffer.to_bytes(8, byteorder='big'))

    message_size = int(message_size)
    message_buffer = int(message_buffer)

    bytes_sent = 0
    number_of_messages = 0
    message = b'0' * message_size

    while bytes_sent < message_size:
        bytes_to_send = min(message_buffer, message_size - bytes_sent)
        chunk = message[bytes_sent:bytes_sent + bytes_to_send]
        data = sock.send(chunk)
        bytes_sent += bytes_to_send
        number_of_messages += 1


    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Numar de mesaje trimise: {number_of_messages}")
    print(f"Numar de bytes trimisi: {bytes_sent}")

    sock.close()


def send_data_TCP_stop_and_wait(localhost, port, message_size, message_buffer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (localhost, port)
    sock.connect(server_address)

    start_time = time.time()

    print("Message size : " + str(message_size) + "   Buffer : " + str(message_buffer))

    # send the message size and buffer to the server
    sent = sock.send(message_size.to_bytes(8, byteorder='big'))
    sent = sock.send(message_buffer.to_bytes(8, byteorder='big'))

    message_size = int(message_size)
    message_buffer = int(message_buffer)

    bytes_sent = 0
    number_of_messages = 0
    message = b'0' * message_size

    while bytes_sent < message_size:
        bytes_to_send = min(message_buffer, message_size - bytes_sent)
        chunk = message[bytes_sent:bytes_sent + bytes_to_send]
        data = sock.send(chunk)
        
        response = sock.recv(message_buffer);
        if(response.decode() == "ACK"): 
            bytes_sent += bytes_to_send
            number_of_messages += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Numar de mesaje trimise: {number_of_messages}")
    print(f"Numar de bytes trimisi: {bytes_sent}")

    sock.close()


def send_data_UDP_streaming(localhost, port, message_size, message_buffer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)

    start_time = time.time()

    print("Message size : " + str(message_size) + "   Buffer : " + str(message_buffer))

    # send the message size and buffer to the server
    sent = sock.sendto(message_size.to_bytes(8, byteorder='big'), server_address)
    sent = sock.sendto(message_buffer.to_bytes(8, byteorder='big'), server_address)

    message_size = int(message_size)
    message_buffer = int(message_buffer)

    bytes_sent = 0
    number_of_messages = 0
    message = b'0' * message_size

    while bytes_sent < message_size:
        bytes_to_send = min(message_buffer, message_size - bytes_sent)
        chunk = message[bytes_sent:bytes_sent + bytes_to_send]
        data = sock.sendto(chunk, server_address)
        bytes_sent += bytes_to_send
        number_of_messages += 1

    end_time = time.time()
    elapsed_time = end_time - start_time


    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Numar de mesaje trimise: {number_of_messages}")
    print(f"Numar de bytes trimisi: {bytes_sent}")

    sock.close()


def send_data_UDP_stop_and_wait(localhost, port, message_size, message_buffer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (localhost, port)

    start_time = time.time()

    print("Message size : " + str(message_size) + "   Buffer : " + str(message_buffer))

    # send the message size and buffer to the server
    sent = sock.sendto(message_size.to_bytes(8, byteorder='big'), server_address)
    sent = sock.sendto(message_buffer.to_bytes(8, byteorder='big'), server_address)

    message_size = int(message_size)
    message_buffer = int(message_buffer)

    bytes_sent = 0
    number_of_messages = 0
    message = b'0' * message_size

    while bytes_sent < message_size:
        bytes_to_send = min(message_buffer, message_size - bytes_sent)
        chunk = message[bytes_sent:bytes_sent + bytes_to_send]
        data = sock.sendto(chunk, server_address)

        response, server_address = sock.recvfrom(message_buffer);
        if(response.decode() == "ACK"): 
            bytes_sent += bytes_to_send
            number_of_messages += 1

    end_time = time.time()
    elapsed_time = end_time - start_time


    print(f"Timpul total de transmisie: {elapsed_time:.3f} secunde")
    print(f"Numar de mesaje trimise: {number_of_messages}")
    print(f"Numar de bytes trimisi: {bytes_sent}")

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
parser.add_argument('-bf', '--buffer_size', type=str, choices=[
      '15500', '32500', '65000'], required=True, help='dimensiunea buffer-ului')


args = parser.parse_args()


if (args.connection.upper() == "TCP"):
    if (args.transfer_mode.lower() == "streaming"):
        send_data_TCP_streaming(args.ip_address, args.port, int(args.size_message), int(args.buffer_size))
    elif (args.transfer_mode.lower() == "stop-and-wait"):
        send_data_TCP_stop_and_wait(args.ip_address, args.port, int(args.size_message), int(args.buffer_size))
    else:
        print("Mecanismul specificat nu este suportat!")
        exit(0)
elif (args.connection.upper() == "UDP"):
    if (args.transfer_mode.lower() == "streaming"):
        send_data_UDP_streaming(args.ip_address, args.port, int(args.size_message), int(args.buffer_size))
    elif (args.transfer_mode.lower() == "stop-and-wait"):
        send_data_UDP_stop_and_wait(args.ip_address, args.port, int(args.size_message), int(args.buffer_size))
    else:
        print("Mecanismul specificat nu este suportat!")
        exit(0)
else:
    print("Protocolul specificat nu este suportat!")
    exit(0)