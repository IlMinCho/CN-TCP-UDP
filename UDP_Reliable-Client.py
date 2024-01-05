import socket
import sys

def udp_client(file_name):
    server_address = '127.0.0.1'
    server_port = 50010

    try:
        with open(file_name, 'r') as f:
            for i in range(7):
                line = f.readline().strip()
                if not line:
                    print("Less than 7 lines in file.")
                    return

                print(f"Input request: {line}")

                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.sendto(line.encode(), (server_address, server_port))
                    data, _ = s.recvfrom(1024)
                    status_code, result = data.decode().split()

                    if status_code == "200":
                        print(f"The result is: {result}")
                    else:
                        print(f"Error {status_code}: -1")  # Using -1 as a generic error message
                    
                    s.close()

    except Exception as e:
        print(f"An error occurred: {e}")
        s.close()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("It should be: python UDP_Client.py <filename>")
        sys.exit(1)
    
    udp_client(sys.argv[1])