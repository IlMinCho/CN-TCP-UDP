import socket
import sys
import random

def perform_operation(oc, num1, num2):
    if oc == '+':
        return 200, num1 + num2
    elif oc == '-':
        return 200, num1 - num2
    elif oc == '*':
        return 200, num1 * num2
    elif oc == '/' and num2 != 0:  # Ensure not dividing by zero
        return 200, num1 / num2
    elif oc == '/' and num2 == 0:  # If division by zero
        return 630, -1
    return 620, -1  # Invalid OC

def udp_server(p, seed):
    random.seed(seed)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        server_address = '127.0.0.1'
        server_port = 50010
        

        s.bind((server_address, server_port))
        s.settimeout(2)
        # print("UDP server started. Waiting for a connection :)")

        try:
            while True:
                try:
                    data, addr = s.recvfrom(1024)
                except socket.timeout:
                    continue

                received_line = data.decode().strip()
                parts = received_line.split()

                # Simulate dropping packets
                if random.random() <= p:
                    print(f"{received_line} -> dropped")
                    continue

                if len(parts) != 3:
                    s.sendto("620 -1".encode(), addr)
                    print(f"{received_line} -> 620 -1")
                    continue

                oc, n1, n2 = parts
                try:
                    n1, n2 = int(n1), int(n2)
                except ValueError:
                    s.sendto("630 -1".encode(), addr)
                    print(f"{received_line} -> 630 -1")
                    continue

                status, result = perform_operation(oc, n1, n2)
                s.sendto(f"{status} {result}".encode(), addr)
                print(f"{received_line} -> {status} {result}")

        except KeyboardInterrupt:
            print("\nServer stopped.")
            s.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("It should be: python UDP_Unreliable-Server.py <probability> <seed>")
        sys.exit(1)

    probability = float(sys.argv[1])
    seed_value = sys.argv[2]

    udp_server(probability, seed_value)