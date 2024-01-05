import socket

def perform_operation(oc, num1, num2):
    if oc == '+':
        return 200, num1 + num2
    elif oc == '-':
        return 200, num1 - num2
    elif oc == '*':
        return 200, num1 * num2
    elif oc == '/' and num2 != 0:
        return 200, num1 / num2
    elif oc == '/' and num2 == 0:
        return 630, -1

    return 620, -1  # Invalid OC

def udp_server():
    server_address = '127.0.0.1'
    server_port = 50010
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((server_address, server_port))
        s.settimeout(2) 
        # print("UDP server started. Waiting for requests :)")

        try:
            while True:
                try:
                    data, addr = s.recvfrom(1024)
                    received_line = data.decode().strip()
                    parts = received_line.split()

                    if len(parts) != 3:
                        response = "620 -1".encode()
                        print(f"{received_line} -> 620 -1")
                    else:
                        oc, n1, n2 = parts
                        try:
                            n1, n2 = int(n1), int(n2)
                            status, result = perform_operation(oc, n1, n2)
                            response = f"{status} {result}".encode()
                            print(f"{received_line} -> {status} {result}")
                        except ValueError:
                            response = "630 -1".encode()
                            print(f"{received_line} -> 630 -1")

                    s.sendto(response, addr)

                except socket.timeout:
                    continue

        except KeyboardInterrupt:
            # print("\nServer stopped.")
            s.close()

if __name__ == "__main__":
    udp_server()