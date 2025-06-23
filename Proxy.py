import socket, ssl

proxy_host = "198.199.86.11"
proxy_port = 8080

target_host = input("Enter website (without https://): ").strip()
target_port = 443

sock = socket.create_connection((proxy_host, proxy_port))

connect_request = f"CONNECT {target_host}:{target_port} HTTP/1.1\r\nHost: {target_host}\r\n\r\n"
sock.sendall(connect_request.encode())

response = sock.recv(4096)
if not (b"200 Connection established" in response or b"200 OK" in response):
    print("Proxy connection failed:")
    print(response.decode(errors="ignore"))
    sock.close()
    exit()

context = ssl.create_default_context()
secure_sock = context.wrap_socket(sock, server_hostname=target_host)

get_request = f"GET / HTTP/1.1\r\nHost: {target_host}\r\nConnection: close\r\n\r\n"
secure_sock.sendall(get_request.encode())

full_response = b""
while True:
    chunk = secure_sock.recv(4096)
    if not chunk:
        break
    full_response += chunk

print(full_response.decode(errors="ignore"))

secure_sock.close()
