# Libraries
import logging
from logging.handlers import RotatingFileHandler
import paramiko
from key_files import host_key
import socket
import threading

# Constants
logging_format = logging.Formatter('%(message)s')
SSH_BANNER = "SSH-2.0-MySSHServer_1.0"

# Loggers and logging files
funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler('audits.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

creds_logger = logging.getLogger('CredsLogger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('cmd_audits.log', maxBytes=2000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)

# Emulated shell
def emulated_shell(channel, client_ip):
    channel.send(b'corporate-jumpbox2$')  # prompt
    command = b""
    while True:
        char = channel.recv(1)
        if not char:
            channel.close()
            break

        channel.send(char)
        command += char

        if char == b'\r':
            stripped_command = command.strip()
            if stripped_command == b'exit':
                response = b'\n Goodbye! \n'
                channel.send(response)
                channel.close()
                break
            elif stripped_command == b'pwd':
                response = b"\n\\usr\\local\r\n"
            elif stripped_command == b'whoami':
                response = b"\ncorpuser\r\n"
            elif stripped_command == b'ls':
                response = b"\njumpbox1.conf\r\n"
            elif stripped_command == b'cat jumpbox1.conf':
                response = b"\nGo to deeboodah.com\r\n"
            else:
                response = b"\n" + stripped_command + b"\r\n"

            creds_logger.info(f"{client_ip}: {stripped_command.decode(errors='ignore')}")
            channel.send(response)
            channel.send(b'corporate-jumpbox2$')
            command = b""

# SSH Server + sockets
class Server(paramiko.ServerInterface):
    def __init__(self, client_ip, input_username=None, input_password=None):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.input_username = input_username
        self.input_password = input_password

    def check_channel_request(self, kind: str, chanid: int):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username):
        return "password"

    def check_auth_password(self, username, password):
        creds_logger.info(f"{self.client_ip}: Username='{username}' Password='{password}'")
        funnel_logger.info(f"Client {self.client_ip} attempted to connect with,  Username='{username}' Password='{password}'")
        if self.input_username is not None and self.input_password is not None:
            if username == self.input_username and password == self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        return True

# Connection handler
def client_handle(client, addr, username, password):
    client_ip = addr[0]
    funnel_logger.info(f"{client_ip} connected to the server.")
    print(f"{client_ip} has connected to the server.")

    try:
        transport = paramiko.Transport(client)
        transport.local_version = SSH_BANNER
        server = Server(client_ip=client_ip, input_username=username, input_password=password)

        transport.add_server_key(host_key)
        transport.start_server(server=server)

        channel = transport.accept(100)
        if channel is None:
            print("No channel was opened")
            return

        channel.send(b"Welcome to the SSH Honeypot\r\n")
        emulated_shell(channel, client_ip=client_ip)

    except Exception as error:
        print(f"Error: {error}")
    finally:
        try:
            transport.close()
        except Exception as error:
            print(f"Transport close error: {error}")
        client.close()

# Start the honeypot server
def honeypot(address, port, username, password):
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks.bind((address, port))
    socks.listen(100)
    print(f"Server listening on port {port}.")

    while True:
        try:
            client, addr = socks.accept()
            ssh_honeypot_thread = threading.Thread(target=client_handle, args=(client, addr, username, password))
            ssh_honeypot_thread.start()
        except Exception as error:
            print(f"Accept error: {error}")

# Run honeypot
honeypot('127.0.0.1', 2223, username= None, password= None)
