from curses import wrapper
from ui import ChatUI
import socket, select, string, sys
import thread
import time

def emissor(serverSocket,ui,lock):
	print "Emissor"
	ui.chatbuffer_add("Receiving")
	while True:
		try:
			msg = serverSocket.recv(4096)
		except socket.timeout, e:
			err = e.args[0]
			# this next if/else is a bit redundant, but illustrates how the
			# timeout exception is setup
			if err == 'timed out':
				#time.sleep(1)
				#print 'recv timed out, retry later'
				continue
			else:
				print e
				ui.chatbuffer_add(err)
				sys.exit(1)
		except socket.error, e:
			# Something else happened, handle error, exit, etc.
			print e
			ui.chatbuffer_add(e.args[0])
			sys.exit(1)
		else:
			if len(msg) == 0:
				print 'orderly shutdown on server end'
				sys.exit(0)
			else:
				ui.chatbuffer_add(msg)

def receptor(serverSocket,ui,lock):
	ui.chatbuffer_add("Chatting")
	inp = ""
	while inp != "/quit":
		inp = ui.wait_input()
		serverSocket.send(inp+"\n")

def main(stdscr):
	stdscr.clear()
	ui = ChatUI(stdscr)

	host = ui.wait_input("Host: ")
	port = int(ui.wait_input("Porta: "))
	username = ui.wait_input("Apelido: ")

	#Connection setup
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)

    # connect to remote host
	try :
		s.connect((host, port))
	except :
		print 'Falha ao conectar com o servidor'
		sys.exit()

	#Regisra o usuario:
	s.send("setUsername->"+username)

	ui.chatbuffer_add('Conectado. Pode mandar mensagens...\n')

	ui.redraw_ui()

	lock = thread.allocate_lock()
	thread.start_new_thread(emissor, (s, ui,lock))
	#thread.start_new_thread(receptor, (s, ui,lock))

	inp = ""
	while inp != "/quit":
		inp = ui.wait_input()
		s.send(inp+" \n")

if __name__ == "__main__":
	wrapper(main)