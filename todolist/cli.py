import curses
import locale
locale.setlocale(locale.LC_ALL, '')

from curses import wrapper

from . import ListBackend

# Get a string with an input box
def inpbox(scr, prompt):
    scr.clear()
    scr.refresh()

    # Parent window
    width = 42
    height = 5
    top = (curses.LINES - height) // 2
    left = (curses.COLS - width) // 2
    box = curses.newwin(height, width, top, left)
    box.bkgd(curses.color_pair(1))
    box.border()
    box.addstr(1, 2, prompt)
    box.refresh()

    # Input box
    txt = curses.newwin(1, width - 4, top + height - 2, left + 2)
    txt.bkgd(curses.color_pair(2))
    txt.refresh()
    txt.keypad(1)
    curses.echo()
    new = txt.getstr().decode('UTF-8')
    curses.noecho()

    scr.clear()
    scr.refresh()
    return new

# Print the contents of a list in a box
def show_list(scr, todo, selected):
    scr.clear()
    scr.refresh()

    width = 40; height = len(todo.lst)
    if height == 0:
        height = 1
    if height > curses.LINES:
        height = curses.LINES - 2
    top = (curses.LINES - height) // 2
    left = (curses.COLS - width) // 2
    win = curses.newwin(height + 2, width + 2, top - 1, left - 1)
    win.bkgd(curses.color_pair(1))
    win.border()

    if todo.lst:
        for i in range(height):
            line = " " + str(i + 1) + ". " + todo.lst[i]
            if len(line) < width:
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
    scr.refresh()
    win.keypad(1)
    char = win.getch()

    return char

#todo: Help bar, cmd argument for file, clear method

def run():
    try:
        wrapper(run_curses)
    except KeyboardInterrupt as _:
        exit(0)

def run_curses(scr):
    # Empty list
    todo = ListBackend.ListBackend()
    todo.load("default.txt")

    # Initialise
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

    selected = -1
    modified = 0

    while 1:
        c = show_list(scr, todo, selected)

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
            if len(todo.lst) != old:
                modified = 1
        elif c == ord('-'):
            old = len(todo.lst)
            todo.del_by_index(selected)
            if selected >= len(todo.lst):
                selected = len(todo.lst) - 1
            if len(todo.lst) != old:
             modified = 1
        elif c == curses.KEY_UP:
            if selected == -1:
                selected = len(todo.lst)
            selected = selected - 1
            if selected < 0:
                selected = 0
        elif c == curses.KEY_DOWN:
            selected = selected + 1
            if selected >= len(todo.lst):
                selected = len(todo.lst) - 1