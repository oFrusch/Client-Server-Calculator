import argparse
import socket
import datetime
import signal
import sys

def udp_server(port_number: int) -> int:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', port_number))

    operators = ('-', '+', '*', '/')

    # run server
    try:
        while True:
            equation, client_addr = server_socket.recvfrom(65535)
            equation_as_str = equation.decode('ascii')
            print('Client sent equation ' + equation_as_str)
            num1 = equation_as_str[0]
            num2 = equation_as_str[2]
            operator = equation_as_str[1]

            if operator not in operators:
                print('invalid operator')
                continue

            if num2 == '0' and operator == '/':
                print('can not divide by 0')
                continue

            try:
                print('Answer to equation: ' + str(eval(equation_as_str)))
                ans = str(eval(equation_as_str))
                ret_ans = "Status Code: 200 - Answer: " + ans
                server_socket.sendto(ret_ans.encode('ascii'), client_addr)
            except:
                print('Invalid Equation')
                ret_ans = "Status Code: 300 - Answer: -1"
                server_socket.sendto(ret_ans.encode('ascii'), client_addr)
    except KeyboardInterrupt:
        print('Exit on Keyboard Interrupt')


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="Provide a port number")
    parse.add_argument('-p', metavar='PORT', type=int, default=50000)
    arguments = parse.parse_args()
    udp_server(arguments.p)