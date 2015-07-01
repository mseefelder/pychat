from curses import wrapper
from ui import ChatUI
import thread
import time

def emissor(ui,lock):
	print "Emissor"
	ui.chatbuffer_add("Receiving")
	while True:
		ui.chatbuffer_add("Threadtest")
		time.sleep(1)

def receptor(ui,lock):
	ui.chatbuffer_add("Chatting")
	inp = ""
	while inp != "/quit":
		inp = ui.wait_input()

def main(stdscr):
	stdscr.clear()
	ui = ChatUI(stdscr)
	lock = thread.allocate_lock()
	thread.start_new_thread(emissor, (ui,lock))
	thread.start_new_thread(receptor, (ui,lock))

	inp = ""
	while inp != "/quit":
		inp = ui.wait_input()

if __name__ == "__main__":
	wrapper(main)