import argparse
import socket
import datetime
import pickle


def udp_client(port_number: int, filename: str, timeout: float):
    with open(filename) as file:
        for line in file:

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # set timeout for non-received packet
            client_socket.settimeout(timeout)

            values = line.split()

            equation = [values[1], values[0], values[2]]

            # send equation as an array of values for ease of validity checking
            equation = pickle.dumps(equation)

            client_socket.sendto(equation, ('127.0.0.1', port_number))

            try:
                answer = client_socket.recv(65535)
            except:
                print("Request Timed Out")
                break

            answer = answer.decode('ascii').split()

            if answer[0] == '200':
                print(answer[1])
            elif answer[0] == '300':
                print('invalid equation submitted')

            client_socket.close()


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="Provide a port number")
    parse.add_argument('-p', metavar='PORT', type=int, default=50000)
    parse.add_argument('-f', metavar='FILE', type=str, default='equations')
    parse.add_argument('-t', metavar='TIMEOUT', type=float, default=5.0)
    arguments = parse.parse_args()
    udp_client(arguments.p, arguments.f, arguments.t)
