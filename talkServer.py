from curses import wrapper
from ui import ChatUI
import socket, select, string, sys
import thread
import time

def receptor(listenerSocket,ui,lock):
	ui.chatbuffer_add("Recebendo.")
	while True:
		try:
			msg = listenerSocket.recv(4096)
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
				print 'Interlocutor desconectado.'
				sys.exit(0)
			else:
				ui.chatbuffer_add("<Interlocutor> " + msg)

def main(stdscr):
	stdscr.clear()
	ui = ChatUI(stdscr)

	RECV_BUFFER = 4096
	PORT = 5000
     
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("0.0.0.0", PORT))
	server_socket.listen(1)

	ui.chatbuffer_add('Host: localhost; '+'Porta: '+str(PORT)+'; \n Aguardando ouvinte...\n')

	listener, addr = server_socket.accept()

	ui.chatbuffer_add('Conectado. Pode mandar mensagens...\n')

	ui.redraw_ui()

	lock = thread.allocate_lock()
	thread.start_new_thread(receptor, (listener, ui, lock))

	inp = ""
	while inp != "/sair":
		inp = ui.wait_input()
		ui.chatbuffer_add("<Eu> "+inp)
		listener.send(inp+" \n")

	sys.exit(1)

if __name__ == "__main__":
	wrapper(main)