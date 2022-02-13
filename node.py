# client
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 8088))
st="I am NODE at 0.0.0.0\n"
client.send(st.encode())

from_server = client.recv(4096)



# server

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(('0.0.0.0', 6676))
serv.listen(5)

while True:
    conn, addr = serv.accept()
    from_client = ''

    while True:
        data = conn.recv(4096)
        if not data: break
        from_client += str(data)
        print (from_client)
        st="I am SERVER\n"
        conn.send(st.encode())

    conn.close()
    print ('client disconnected')

client.close()

print (from_server)