import socket
import sys

def main(argv):
    if len(argv) == 3:
        transport_type = argv[1]
        if transport_type == 'TCP':
            create_tcp_server(argv[2])
        elif transport_type == 'UDP':
            create_udp_server(argv[2])
        else:
            print('Transport layer type must be TCP or UDP')
    else:
        print('Please provide transport type and port number')

"""
Servers
"""
def create_tcp_server(server_port):
    if server_port.isdigit():
        # AF_INET == IPv4 and SOCK_STREAM == TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', int(server_port)))
        server_socket.listen()
        print('The server is listening for a connection...')
        while True:
            connection_socket, addr = server_socket.accept()
            print('Connection established!\n')

            while True:

                client_input = None
                try:
                    client_input = connection_socket.recv(33).decode()
                except socket.error:
                    print('Error grabbing client input. Please wait...\n')
                    continue

                if not client_input:
                    print('Client program has closed. Waiting for new client connection...')
                    break
                else:
                    if len(client_input) == 33:
                        op_result = ''
                        num1, num2, operand = grab_numbers(client_input)
                        valid_operands = ['+', '-', '/', '*']
                        if operand not in valid_operands:
                            error_message = 'ERR: Invalid operand'
                            op_result = ('\0' * 16) + error_message.ljust(32, '\0')
                        else:
                            if not (isfloat(num1[1:]) and isfloat(num2[1:])):
                                error_message = 'ERR: Not valid numbers'
                                op_result = ('\0' * 16) + error_message.ljust(32, '\0')
                            else:
                                if float(num2[1:]) == 0.0 and operand == '/':
                                    error_message = 'ERR: Divide by zero'
                                    op_result = ('\0' * 16) + error_message.ljust(32, '\0')
                                else:
                                    success_message = "Brought to you by Kevin's server"
                                    result = perform_operation(num1, num2, operand)
                                    if result >= 0:
                                        op_result = '+' + str(result).ljust(15, '\0') + success_message.ljust(32, '\0')
                                    else:
                                        op_result = str(result).ljust(16, '\0') + success_message.ljust(32, '\0')

                        connection_socket.send(op_result.encode())
                    else:
                        error_message = 'ERROR: Not valid input'
                        op_result = ('\0' * 16) + error_message.ljust(32, '\0')
                        server_socket.sendto(op_result.encode(), client_address)

            connection_socket.close()
    else:
        print('Please use a valid port number')

def create_udp_server(server_port):
    if server_port.isdigit():
        # AF_INET == IPv4 and SOCK_DGRAM == UDP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('', int(server_port)))
        print('The server is accepting messages...')

        while True:

            client_input = None
            client_address = None
            try:
                client_input, client_address = server_socket.recvfrom(33)
                print('Received message from client at ' + client_address[0] + '\n')
            except socket.error:
                print('No messages right now. Looking again...')
                continue

            if (not client_input) or (not client_address):
                print('No messages right now. Looking again...')
                continue
            else:
                client_input = client_input.decode()

                if len(client_input) == 33:
                    op_result = ''
                    num1, num2, operand = grab_numbers(client_input)
                    valid_operands = ['+', '-', '/', '*']
                    if operand not in valid_operands:
                        error_message = 'ERR: Invalid operand'
                        op_result = ('\0' * 16) + error_message.ljust(32, '\0')
                    else:
                        if not (isfloat(num1[1:]) and isfloat(num2[1:])):
                            error_message = 'ERR: Not valid numbers'
                            op_result = ('\0' * 16) + error_message.ljust(32, '\0')
                        else:
                            if float(num2[1:]) == 0.0 and operand == '/':
                                error_message = 'ERR: Divide by zero'
                                op_result = ('\0' * 16) + error_message.ljust(32, '\0')
                            else:
                                success_message = "Brought to you by Kevin's server"
                                result = perform_operation(num1, num2, operand)
                                if result >= 0:
                                    op_result = '+' + str(result).ljust(15, '\0') + success_message.ljust(32, '\0')
                                else:
                                    op_result = str(result).ljust(16, '\0') + success_message.ljust(32, '\0')

                    server_socket.sendto(op_result.encode(), client_address)
                else:
                    error_message = 'ERROR: Not valid input'
                    op_result = ('\0' * 16) + error_message.ljust(32, '\0')
                    server_socket.sendto(op_result.encode(), client_address)

    else:
        print('Please use a valid port number')

"""
Helper Methods
"""
# Method to check if a number is a valid float
def isfloat(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

# Method to perform an operation given tw onumbers and an operand
def perform_operation(num1, num2, operand):
    # num1, num2, and operand are all valid strings at this point
    if operand == '+':
        return apply_sign(num1) + apply_sign(num2)
    elif operand == '-':
        return apply_sign(num1) - apply_sign(num2)
    elif operand == '/':
        return apply_sign(num1) / apply_sign(num2)
    elif operand == '*':
        return apply_sign(num1) * apply_sign(num2)
    else:
        return None

# Method to apply the proper sign to a number
def apply_sign(num):
    if num[0] == '-':
        return float(num[1:]) * -1

    return float(num[1:])

# Method to extract numbers and operand from client input message
def grab_numbers(client_input):
    num1 = None
    num2 = None
    operand = 'x'

    if len(client_input) == 33:
        num1 = client_input[0:16]
        num2 = client_input[16:32]
        operand = client_input[32]

        return num1, num2, operand

    return num1, num2, operand

if __name__ == '__main__':
    main(sys.argv)
