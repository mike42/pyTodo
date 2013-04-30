import curses
import locale

class ListBackend:
	""" Class to help manage the todo-list data structure in an array
	"""
	def __init__(self):
		self.lst = []
		self.fname = ""

	def load(self, fname):
		self.fname = fname
		f = open(fname)
		for line in f:
			self.append(line)
		f.close()

	def save(self):
		if(self.fname == ""):
			return;
		f = open(self.fname, 'w')
		for i in range(0, len(self.lst)):
			f.write(self.lst[i] + "\n")
		f.close()
		
	def delByIndex(self, index):
		if(index < 0):
			# Too small. Ignore
			return;
		if(index >= len(self.lst)):
			# Too large. Ignore
			return;
		for i in range(index, len(self.lst) - 1):
			self.lst[i] = self.lst[i+1]
		self.lst.pop()

	def append(self, item):
		if item != "":
			self.lst.append(item.strip("\n"))


# Get a string with an input box
def inpbox(scr, prompt):
	scr.clear()
	scr.refresh()

	# Parent window
	width = 42; height = 5
	top = (curses.LINES - height) / 2
	left = (curses.COLS - width) / 2
	box = curses.newwin(height, width, top, left)
	box.bkgd(curses.color_pair(1))
	box.border('|', '|', '-', '-', '+', '+', '+', '+')
	box.addstr(1, 2, prompt)
	box.refresh()

	# Input box
	txt = curses.newwin(1, width - 4, top + height - 2, left + 2)
	txt.bkgd(curses.color_pair(2))
	txt.refresh()
	txt.keypad(1)
	curses.echo()
	new = txt.getstr()
	curses.noecho()

	del txt
	del box

	scr.clear()
	scr.refresh()
	return new

# Print the contents of a list in a box
def showList(scr, todo, selected):
	scr.clear()
	scr.refresh()

	width = 40; height = len(todo.lst)
	if height == 0:
		height = 1
	if height > curses.LINES:
		height = curses.LINES - 2
	top = (curses.LINES - height) / 2
	left = (curses.COLS - width) / 2
	win = curses.newwin(height + 2, width + 2, top - 1, left - 1)
	win.bkgd(curses.color_pair(1))
	win.border('|', '|', '-', '-', '+', '+', '+', '+')

	if len(todo.lst) > 0:
		for i in range(0, height):
			line = " " + str(i + 1) + ". " + todo.lst[i]
			if(len(line) < width):
				line = line + ' ' * (width - len(line))
			else:
				line = line[:width-3] + "..."
			if selected == i:
				win.addstr(i + 1, 1, line, curses.color_pair(3))
			else:
				win.addstr(i + 1, 1, line)
	else:
		win.addstr(1, 1," < The todo list is empty! >")
	win.refresh()
	scr.move(curses.LINES - 1, curses.COLS - 1)
	scr.refresh()
	win.keypad(1)
	char = win.getch()
	del win
	return char

#todo: Help bar, cmd argument for file, clear method

# Initialise
scr = curses.initscr()
curses.start_color()

# Colour pairs
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)

# Disable echo
curses.noecho()
scr.keypad(1)
curses.cbreak()

# Set background
scr.bkgd(curses.color_pair(2))
scr.refresh()

# Empty list
todo = ListBackend()
todo.load("default.txt")

selected = -1
modified = 0

while 1:
	c = showList(scr, todo, selected)

	if c == ord('q'):
		if modified == 1:
			todo.save()
		break
	elif c == ord('s'):
		todo.save()
	elif c == ord('+'):
		new = inpbox(scr, "New item")
		old = len(todo.lst)
		todo.append(new)
		if(len(todo.lst) != old):
			modified = 1
	elif c == ord('-'):
		old = len(todo.lst)
		todo.delByIndex(selected)
		if(selected >= len(todo.lst)):
			selected = len(todo.lst) - 1
		if(len(todo.lst) != old):
		 modified = 1
	elif c == curses.KEY_UP:
		if selected == -1:
			selected = len(todo.lst)
		selected = selected - 1
		if(selected < 0):
			selected = 0
	elif c == curses.KEY_DOWN:
		selected = selected + 1
		if(selected >= len(todo.lst)):
			selected = len(todo.lst) - 1


curses.nocbreak()
scr.keypad(0)
curses.echo()
curses.endwin()


