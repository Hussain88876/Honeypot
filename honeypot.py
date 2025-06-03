import argparse
from ssh_honeypot import *
import paramiko

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', type=str, required=True, help="Host's IP address")
    parser.add_argument('-p', '--port', type=int, required=True, help="Host port")
    parser.add_argument('-u', '--username', type=str, help='Username')
    parser.add_argument('-pw', '--password', type=str, help='Password')

    parser.add_argument('-s', '--ssh', action='store_true', help='Run SSH honeypot')
    parser.add_argument('-w', '--http', action='store_true', help='Run HTTP honeypot')

    args = parser.parse_args()

    try:
        if args.ssh:
            print("[-] Running SSH Honeypot....")
            honeypot(args.address, args.port, args.username, args.password)
        elif args.http:
            print("[-] Running HTTP Honeypot....")
            pass
        else:
            print("[!] Choose either --ssh or --http")
    except Exception as e:
        print(f"\n[!] Exiting Honeypot due to error: {e}")
