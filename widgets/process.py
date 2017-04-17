import urwid

from listbox import create_list


class Process(urwid.Frame):
    def __init__(self, app):
        self.app = app
        self.use_hex = False

        self.columns = urwid.Columns([
            ("weight", 0.25, urwid.Pile([urwid.Text('sh')])),
            ("weight", 0.25, urwid.Pile([urwid.Text("x")])),
            ("weight", 0.25, urwid.Pile([urwid.Text("y")])),
            ("weight", 0.25, urwid.Pile([urwid.Text("z")])),
        ])

        self.files = urwid.SimpleFocusListWalker([])
        self.arguments = urwid.SimpleFocusListWalker([])
        self.widget = urwid.Pile([
            ('pack', urwid.Divider()),
            ('pack', urwid.AttrMap(urwid.Text("Arguments: "), 'h2')),
            (3, urwid.ListBox(self.arguments)),
            ('pack', urwid.Divider()),
            ('pack', self.columns),
            ('pack', urwid.AttrMap(urwid.Text("Files: "), 'h2')),
            urwid.ListBox(self.files)
        ])

        super().__init__(self.widget, header=urwid.Text(""))

    def populate(self, process):
        items = []
        self.dict = {}

        for file in  process['descriptors']:
            if file['type'] == 'file':
                items.append(file['path'])
                self.dict[file['path']] = file

        #self.columns[0][0].set_text(process['executable'])

        self.header.set_text(process['executable'])
        self.arguments.extend(create_list(process['arguments']))

        self.files.clear()
        self.files.extend(create_list(items))

    def keypress(self, l, key):
        super().keypress(l, key)
        if key == "left":
            self.app.home()
        elif key in ["r", "w"]:
            column = {"r": "read_content", "w": "write_content"}[key]
            program = "hx" if self.use_hex else "vim"

            if column in self.dict[self.focus[6].focus.original_widget.text]:
                self.app.open_file(self.dict[self.focus[6].focus.original_widget.text][column], program=program)
        elif key == "x":
            self.use_hex = not self.use_hex
