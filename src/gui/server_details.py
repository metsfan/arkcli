from tkinter import *


class ServerDetailsWidget:
    def __init__(self, window, app):
        self.container = Frame(window)
        self.container.grid(row=1,column=0)

        self.server_status_text = Label(self.container, text="Server Status: Not Running")
        self.server_status_text.grid(row=0, column=0, padx=15, pady=10)

        self.buttons_container = Frame(self.container)
        self.buttons_container.grid(row=1, column=0, padx=15, pady=10)

        self.start_button = Button(self.buttons_container, text="Start", command=app.start_server, width=10)
        self.start_button.grid(row=0, column=0, padx=15)
        self.start_button.config(state=DISABLED)

        self.stop_button = Button(self.buttons_container, text="Stop", command=app.stop_server, width=10)
        self.stop_button.grid(row=0, column=1, padx=15)
        self.stop_button.config(state=DISABLED)

        self.restart_button = Button(self.buttons_container, text="Restart", command=app.restart_server, width=10)
        self.restart_button.grid(row=0, column=2, padx=15)
        self.restart_button.config(state=DISABLED)

    def hide(self):
        self.container.forget()

    def show(self):
        self.container.grid(row=1,column=0)

