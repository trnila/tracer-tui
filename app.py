import os

import urwid

from listbox import create_list
from widgets.file import File
from widgets.process import Process


class Procese(urwid.ListBox):
    def keypress(self, l, key):
        super().keypress(l, key)
        if key in ["enter", "right"]:
            app.show_process(self.focus.original_widget.data.data['pid'])
        return key


class DataProcess:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "[{}] {}".format(self.data['pid'], self.data['executable'])


class App:
    def __init__(self):
        palette = [
            ('reveal focus', 'black', 'dark cyan', 'standout'),
            ('h2', 'dark cyan', 'black', 'bold'),
        ]

        proc = [
            DataProcess(proc)
            for pid, proc in data['processes'].items()
            ]

        content = create_list(proc)

        self.listbox = Procese(content)
        self.loop = urwid.MainLoop(
            self.listbox,
            palette=palette,
            unhandled_input=self.unhandled_input
        )

        self.process = Process(self)
        self.file = File()

    def unhandled_input(self, key):
        if key == "q":
            raise urwid.ExitMainLoop()

    def home(self):
        self.render(self.listbox)

    def show_process(self, pid):
        self.process.populate(data['processes'][str(pid)])
        self.render(self.process)

    def open_file(self, path):
        self.loop.stop()
        os.system("vim " + path)
        self.loop.start()

    def run(self):
        self.loop.run()

    def render(self, widget):
        self.loop.widget = widget
        self.loop.widget._invalidate()
        self.loop.draw_screen()


import json

data = json.load(open("/tmp/data.json"))

app = App()
app.run()
