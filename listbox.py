import urwid


class SelectableText(urwid.Text):
    def __init__(self, markup):
        super().__init__(str(markup))
        self.data = markup

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

def create_list(items):
    return urwid.SimpleListWalker([
         urwid.AttrMap(SelectableText(i), '', 'reveal focus')
         for i in items]
    )
