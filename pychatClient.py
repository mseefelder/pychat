# telnet program example
import socket, select, string, sys
 
def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        print 'Uso : python pychatClient.py host porta apelido \n Example: python pychatClient.py localhost 5000 Zeca'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
    username = sys.argv[3]
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Falha ao conectar com o servidor'
        sys.exit()

    s.send("setUsername->"+username)
    prompt()
     
    print 'Conectado. Pode mandar mensagens...'
    prompt()
     
    while True:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDesconectado.'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
             
            #user entered a message
            else :
               	msg = sys.stdin.readline()
		a = msg[:-1]
		a = a.replace(" ","")
		if str(a[:]) == "exit":
			s.send(msg)
			s.shutdown(1)	
		else:
                	s.send(msg)	
        	        prompt()
