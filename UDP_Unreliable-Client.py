import socket
import sys
import time

def udp_client(file_name):
    server_address = ('127.0.0.1', 50010)
    
    with open(file_name, 'r') as f:
        for _ in range(7):  # Repeat the process for 7 lines
            line = f.readline().strip()
            if not line:  # Break if no more lines to read
                break

            d = 0.1  # Initial timer value
            while d <= 2:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.settimeout(d)  # set the socket timeout
                    try:
                        s.sendto(line.encode(), server_address)
                        
                        data, _ = s.recvfrom(1024)
                        status_code, result = data.decode().split()
                        status_code = int(status_code)
                        
                        if status_code == 200:
                            print(f"Result is {result}")
                        else:
                            print(f"Error {status_code}: {result}")
                        s.close()
                        break
                    except socket.timeout:
                        d *= 2
                        if d > 2:
                            print("Request timed out: the server is DEAD")
                            break
                        print("Request timed out: resending")
                    
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        s.close()
                        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python UDP_Unreliable-Client.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    udp_client(file_name)