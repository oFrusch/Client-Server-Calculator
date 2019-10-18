import argparse
import socket
import datetime
import sys, signal
import pickle


def check_valid_operation(operation: list) -> bool:
    if not operation:
        return False

    operators = set()
    operators.add('-')
    operators.add('+')
    operators.add('*')
    operators.add('/')

    # check for invalid operator
    if operation[1] not in operators:
        return False

    # check for division by 0
    if operation[2] == '0' and operation[1] == '/':
        return False

    # make sure values are integers
    try:
        int(operation[0])
        int(operation[2])
    except:
        return False

    return True


def udp_server(port_number: int) -> int:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', port_number))

    # run server
    try:
        while True:
            equation, client_addr = server_socket.recvfrom(65535)

            # receive equation as a list of strings
            equation = pickle.loads(equation)
            equation_as_str = ''.join(equation)

            print('Client sent equation ' + equation_as_str)

            # invalid operator or division by 0
            if not check_valid_operation(equation):
                print('Invalid Equation')
                ret_ans = "300 -1"
                server_socket.sendto(ret_ans.encode('ascii'), client_addr)
                continue

            try:
                print('Answer to equation: ' + str(eval(equation_as_str)))
                ans = str(eval(equation_as_str))
                ret_ans = "200 " + ans
                server_socket.sendto(ret_ans.encode('ascii'), client_addr)
            except:
                print('Invalid Equation')
                ret_ans = "300 -1"
                server_socket.sendto(ret_ans.encode('ascii'), client_addr)

    except KeyboardInterrupt:
        print('Server Offline')


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="Provide a port number")
    parse.add_argument('-p', metavar='PORT', type=int, default=50000)
    arguments = parse.parse_args()
    udp_server(arguments.p)
