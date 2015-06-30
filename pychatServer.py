# Tcp Chat server
 
import socket, select
 
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
                print "Client %s is offline" % USERNAMES[str(socket.getpeername())]
                del USERNAMES[str(socket.getpeername())]
 
if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    REMOVED_SOCKETS = []
    USERNAMES = {}
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                USERNAMES[str(sockfd.getpeername())] = "Sem nome"
                print "Client (%s, %s) connected" % addr
             
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        if data.startswith("setUsername->"):
                            USERNAMES[str(sock.getpeername())] = data.replace("setUsername->","",1)
                            print "New username: %s" % USERNAMES[str(sock.getpeername())]
                            broadcast_data(sock, "\r" + '<' + USERNAMES[str(sock.getpeername())] + '> entrou na conversa\n')
                        else:
			    a = data[:-1]
			    if str(a) == "exit":				
				usuario = USERNAMES[str(sock.getpeername())]
				#inform = "O usuario " + str(usuario) + " foi desconectado!"
				#broadcast_data(sock, "\r" + inform)
				REMOVED_SOCKETS.append(sock)
				sock.close()
				CONNECTION_LIST.remove(sock)
				
                    		del USERNAMES[str(sock.getpeername())]
			    else:
				broadcast_data(sock, "\r" + '<' + USERNAMES[str(sock.getpeername())] + '> ' + data)                
                 
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
		    if (sock in REMOVED_SOCKETS) == False:
		    	CONNECTION_LIST.remove(sock)
                    	del USERNAMES[str(sock.getpeername())]
                    	continue
     
    server_socket.close()
