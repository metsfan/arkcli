from tkinter import *


class ServerNameWidget:
    def __init__(self, window, app):
        self.app = app

        self.container = Frame(window)
        self.container.grid(column=0, row=0)

        self.name_entry = Entry(self.container, width=30)
        self.name_entry.grid(column=0, row=0)

        self.use_button = Button(self.container, text="Use", command=self.set_current_server)
        self.use_button.grid(column=1, row=0)

    def set_current_server(self):
        self.app.on_server_changed(self.name_entry.get())