from curses import wrapper
from ui import ChatUI
import socket, select, string, sys
from threading import Thread
from time import sleep

def receptor(serverSocket, ui):
	while 1:
		#msg = serverSocket.recv(4096)
		#if not msg: break
		#ui.chatbuffer_add(msg)
		try:
			msg = serverSocket.recv(4096)
		except socket.timeout, e:
			err = e.args[0]
			if err == 'timed out':
				sleep(1)
				print 'recv timed out, retry later'
				continue
			else:
				print e
				sys.exit(1)
		except socket.error, e:
			print e
			sys.exit(1)
		else:
			#if len(msg) == 0;
			if not msg:
				#print 'orderly shutdown on server end'
				#sys.exit(0)
				break
			else:
				ui.chatbuffer_add(msg)

def emissor(serverSocket, ui):
	msg = ""
	while msg != "/quit":
		msg = ui.wait_input()
		serverSocket.send(msg)

def main(stdscr):
	stdscr.clear()
	ui = ChatUI(stdscr)
	host = ui.wait_input("Host: ")
	port = int(ui.wait_input("Porta: "))
	username = ui.wait_input("Apelido: ")
	ui.userlist.append(username)
	ui.redraw_userlist()

	#Connection setup
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
     
	# connect to remote host
	try :
		s.connect((host, port))
	except :
		ui.chatbuffer_add('Falha ao conectar com o servidor')
		sys.exit()

	#Registra o usuario:
	s.send("setUsername->"+username)

	ui.chatbuffer_add('Conectado. Pode mandar mensagens...\n')


	#Thread do Emissor

	class TEmissor(Thread):
		def __init__ (self):
			Thread.__init__(self)

		def run (self):
			emissor(s, ui)

	class TReceptor(Thread):
		def __init__ (self):
			Thread.__init__(self)

		def run (self):
			receptor(s, ui)

    #TO DO: Chamar as duas threads aqui:

	em = TEmissor()
	re = TReceptor()
	em.start()
	re.start()

   
    #thread.start_new_thread(receptor, (s, ui))
    #thread.start_new_thread(emissor, (s))

    #TALVEZ tenha que usar locks: serverSocket.recv(4096) no receptor trava 
    #enquanto nao recebe nada do servidor.
    #a boa eh colocar um timeout e lock.aquire() espera mensagem por
    #um tempo e se nao vier lock.release().
    #tem q ver se eh necessario no emissor tb

if __name__ == "__main__":

	wrapper(main)
