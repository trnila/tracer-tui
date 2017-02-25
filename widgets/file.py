import urwid

from listbox import create_list


class File(urwid.Frame):
    def __init__(self):
        self.content = urwid.SimpleFocusListWalker([])
        super().__init__(urwid.ListBox(self.content))

    def open(self, path):
        with open(path) as f:
            lines = f.read().splitlines()
            self.content.extend(create_list(lines))