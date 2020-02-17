from src.command.command import Command
from valve.rcon import execute, RCONMessage, RCONCommunicationError, RCONAuthenticationError, RCONMessageError


class RconCommand(Command):
    def __init__(self, name, command):
        self.name = name
        self.command = command

    def run(self, config):
        address = ("127.0.0.1", config["RCONPort"])
        password = config["adminPassword"]

        try:
            response = execute(address, password, self.command)
            print("RCON command successful")
            print(response)
        except RCONCommunicationError:
            print("Failed to execute RCON command")
        except RCONAuthenticationError:
            print("Failed to authenticate RCON request")
        except RCONMessageError:
            print("RCON command not well formed")
