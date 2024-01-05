import socket

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


def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        server_address='127.0.0.1'
        server_port=50010

        s.bind((server_address, server_port))
        s.listen()
        s.settimeout(2)

        # print("TCP server started. Waiting for a connection :)")
        try:
            while True:
                try:
                    conn, addr = s.accept()
                except socket.timeout:
                    continue

                with conn:
                    # print(f"Connected by {addr}")
                    data = conn.recv(1024)
                    if not data:
                        break

                    received_line = data.decode().strip()
                    parts = received_line.split()

                    # Check if the received data has the correct format
                    if len(parts) != 3:
                        conn.sendall("620 -1".encode())  # Invalid format
                        print(f"{received_line} -> 620 -1")
                        continue

                    oc, n1, n2 = parts
                    try:
                        n1, n2 = int(n1), int(n2)
                    except ValueError:
                        conn.sendall("630 -1".encode())  # Operand not integer
                        print(f"{received_line} -> 630 -1")
                        continue

                    status, result = perform_operation(oc, n1, n2)
                    conn.sendall(f"{status} {result}".encode())
                    print(f"{received_line} -> {status} {result}")

        except KeyboardInterrupt:
            # print("\nServer stopped.")
            s.close()


if __name__ == "__main__":
    tcp_server()

