from curses import wrapper
from ui import ChatUI
import socket, select, string, sys
import thread

def receptor(serverSocket, ui):
	while 1:
		msg = serverSocket.recv(4096)
		if not msg: break
		ui.chatbuffer_add(msg)

def emissor(serverSocket):
	msg = ""
    while msg != "/quit":
        msg = ui.wait_input()
    serverSocket.send(msg)

def main(stdscr):
    stdscr.clear()
    ui = ChatUI(stdscr)
    host = ui.wait_input("Host: ")
    port = ui.wait_input("Porta: ")
    username = ui.wait_input("Apelido: ")

    #Connection setup
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Falha ao conectar com o servidor'
        sys.exit()

    #Regisra o usuario:
    s.send("setUsername->"+username)

    ui.chatbuffer_add('Conectado. Pode mandar mensagens...\n')

    #TO DO: Chamar as duas threads aqui:
    thread.start_new_thread(receptor, (s, ui))
    thread.start_new_thread(emissor, (s))
    #TALVEZ tenha que usar locks: serverSocket.recv(4096) no receptor trava 
    #enquanto nao recebe nada do servidor.
    #a boa eh colocar um timeout e lock.aquire() espera mensagem por
    #um tempo e se nao vier lock.release().
    #tem q ver se eh necessario no emissor tb

if __name__ == "__main__":

	wrapper(main)