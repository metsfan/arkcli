from src.command.command import Command


class StatusCommand(Command):
    def __init__(self, name):
        self.name = name

    def run(self, config):
        pass