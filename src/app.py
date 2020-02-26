from tkinter import Tk

from src.gui.server_details import ServerDetailsWidget
from src.gui.server_name import ServerNameWidget


class App:
    def __init__(self):
        self.window = Tk()

        self.window.title("Metsfan's Simple Ark Manager (Open Source)")
        self.window.geometry("500x300")

        self.name_widget = ServerNameWidget(self.window, self)

        self.server_details_widget = ServerDetailsWidget(self.window, self)
        self.server_details_widget.hide()

        self.server_name = None

    def run(self):
        self.window.mainloop()

    def on_server_changed(self, name):
        self.server_name = name
        print("Changed to server " + name)

    def start_server(self):
        print("Starting server " + self.server_name)

    def stop_server(self):
        print("Stopping server " + self.server_name)

    def restart_server(self):
        print("Restarting server " + self.server_name)


App().run()