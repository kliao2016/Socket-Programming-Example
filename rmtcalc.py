import socket
import sys

def main(argv):

    if len(argv) == 4:
        transport_type = argv[1]
        if transport_type == 'TCP':
            create_tcp_client(argv[2], argv[3])
        elif transport_type == 'UDP':
            create_udp_client(argv[2], argv[3])
        else:
            print('Transport layer type must be TCP or UDP')
    else:
        print('Please provide transport type, server name, and port number')

"""
Clients
"""
def create_tcp_client(server_name, server_port):
    if server_port.isdigit():
        # AF_INET == IPv4 and SOCK_STREAM == TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            host_name = socket.gethostbyname(server_name)

            # Create connection with server
            client_socket.connect((host_name, int(server_port)))
            print('Connection successful!\n\n')
        except socket.error:
            print('Could not connect to server. Please try again.')
            return None

        while True:
            expression = input('Please type an operation: ')
            if expression and expression == 'quit':
                break

            if expression and validate_message(expression):
                padded_expression = create_padded_message(expression)

                # Send message with proper protocol
                client_socket.send(padded_expression.encode())
            else:
                print('Please enter valid numbers\n')
                continue

            response = None
            try:
                response = client_socket.recv(48).decode()
            except socket.error:
                print('Server could not complete operation. Try again\n')
                continue

            if not response:
                print('Server could not complete operation. Try again\n')
                continue
            else:
                if len(response) == 48:
                    if response[16] == 'E': # There was an error
                        print(response[16:] + '\n')
                    else:
                        print('Result = ' + response[0:16] + ' (' + response[16:] + ')\n')
                else:
                    print('Server returned invalid response\n')
                    continue


        print('Bye...\n')
        client_socket.close()
    else:
        print('Please use a valid port number')

def create_udp_client(server_name, server_port):
    if server_port.isdigit():
        # AF_INET == IPv4 and SOCK_DGRAM == UDP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        host_name = None
        try:
            host_name = socket.gethostbyname(server_name)
        except socket.error:
            print('Invalid server name. Please try again.\n')
            return None

        while True:
            expression = input('Please type an operation: ')
            if expression and expression == 'quit':
                break

            if expression and validate_message(expression):
                padded_expression = create_padded_message(expression)
                client_socket.sendto(padded_expression.encode(), (host_name, int(server_port)))
            else:
                print('Please enter valid numbers\n')
                continue

            response = None
            server_address = None
            try:
                response, server_address = client_socket.recvfrom(48)
                print('Received server response from address ' + server_address[0] + ':')
            except socket.error:
                print('Server could not complete operation. Try again\n')
                continue

            if (not response) or (not server_address):
                print('Server could not complete operation. Try again\n')
                continue
            else:
                response = response.decode()
                if len(response) == 48:
                    if response[16] == 'E': # There was an error
                        print(response[16:] + '\n')
                    else:
                        print('Result = ' + response[0:16] + ' (' + response[16:] + ')\n')
                else:
                    print('Server returned invalid response\n')
                    continue


        print('Bye...\n')
        client_socket.close()
    else:
        print('Please use a valid port number')


"""
Helper Methods
"""
# Method to create the proper padded message
def create_padded_message(expression):
    # Guaranteed that expression has valid numbers
    expression_details = expression.split()
    padded_expression = ''

    # Add padding for numbers to match data protocol
    if expression_details[0][0] in ('-', '+'):
        if expression_details[0][0] == '-':
            padded_expression = '-' + pad_bytes(expression_details[0][1:], True)
        else:
            padded_expression = '+' + pad_bytes(expression_details[0][1:], True)
    else:
        padded_expression = pad_bytes(expression_details[0], False)

    if expression_details[2][0] in ('-', '+'):
        if expression_details[2][0] == '-':
            padded_expression += '-' + pad_bytes(expression_details[2][1:], True)
        else:
            padded_expression += '+' + pad_bytes(expression_details[2][1:], True)
    else:
        padded_expression += pad_bytes(expression_details[2], False)

    padded_expression += expression_details[1]

    return padded_expression

# Method to pad numbers with zeroes
def pad_bytes(number, has_sign):
    length = len(number)
    padded_num = number

    if has_sign:
        if len(number) < 15:
            if number.isdigit():
                # We need the decimal so we don't change the value of the number
                padded_num += '.'
                padded_num = padded_num.ljust(15, '0')
            else:
                padded_num = padded_num.ljust(15, '0')
        else:
            return number
    else:
        if len(number) < 16:
            padded_num = '+' + padded_num
            if number.isdigit():
                padded_num += '.'
                padded_num = padded_num.ljust(16, '0')
            else:
                padded_num = padded_num.ljust(16, '0')

        else:
            return number

    return padded_num

# Method to make sure user input has valid numbers
def validate_message(expression):
    expression_details = expression.split()
    valid = True

    if len(expression_details) < 3 or len(expression_details) > 3:
        return False
    else:
        if not (validate_number(expression_details[0]) and validate_number(expression_details[2])):
            valid = False

    return valid

# Method to ensure the number is a valid integer or decimal
def validate_number(number):
    if number[0] in ('-', '+'):
        return isfloat(number[1:])

    return isfloat(number)

# Method to check if a number is a valid float
def isfloat(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    main(sys.argv)
