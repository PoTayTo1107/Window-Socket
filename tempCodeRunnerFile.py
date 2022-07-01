 self.listNotes.focus_set()
        children = self.listNotes.get_children()
        if children:
            self.listNotes.focus(children[0])
            self.listNotes.selection_set(children[0])