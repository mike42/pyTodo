class ListBackend(object):
    """
    Class to help manage the todo-list data structure in an array
    """
    def __init__(self):
        self.lst = []
        self.fname = None

    def load(self, fname):
        self.fname = fname
        with open(fname, 'r') as f:
            for line in f:
                self.append(line)

    def save(self):
        if self.fname is None:
            return
        with open(self.fname, 'w') as f:
            for line in self.lst:
                f.write(line + "\n")

    def del_by_index(self, index):
        if index < 0:
            # Too small. Ignore
            return
        if index >= len(self.lst):
            # Too large. Ignore
            return
        del self.lst[index]

    def append(self, item):
        if item != "":
            self.lst.append(item.strip("\n"))
