from curses import wrapper
from ui import ChatUI
import socket, select, string, sys
import thread
import time

def receptor(serverSocket,ui,lock):
	ui.chatbuffer_add("Recebendo")
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
				print 'Servidor fechado. Parando de receber.'
				sys.exit(0)
			else:
				ui.chatbuffer_add("<Interlocutor> "+msg)

def main(stdscr):
	stdscr.clear()
	ui = ChatUI(stdscr)

	host = ui.wait_input("Host: ")
	port = int(ui.wait_input("Porta: "))

	#Connection setup
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)

    # conecta ao host remoto
	try :
		s.connect((host, port))
	except :
		print 'Falha ao conectar com o servidor'
		sys.exit()

	ui.chatbuffer_add('Conectado. Pode mandar mensagens...\n')

	ui.redraw_ui()

	lock = thread.allocate_lock()
	thread.start_new_thread(receptor, (s, ui,lock))

	msg = ""
	while msg != "/sair":
		msg = ui.wait_input()
		ui.chatbuffer_add("<Eu> "+msg)
		s.send(msg+" \n")

	sys.exit(1)

if __name__ == "__main__":
	wrapper(main)