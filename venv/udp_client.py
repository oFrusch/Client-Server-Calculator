import argparse
import socket
import datetime

def udp_client(port_number: int):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    operand = input("Please enter an operand: ")
    num1 = input("Please enter your first number: ")
    num2 = input("Please enter your second number: ")

    equation = num1 + operand + num2
    equation = equation.encode('ascii')

    client_socket.sendto(equation, ('127.0.0.1', port_number))

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="Provide a port number")
    parse.add_argument('-p', metavar='PORT', type=int, default=50000)
    arguments = parse.parse_args()
    udp_client(arguments.p)