import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 6676))
st="I am CLIENT at 10.0.0.1\n"
client.send(st.encode())

from_server = client.recv(4096)

client.close()

print (from_server)