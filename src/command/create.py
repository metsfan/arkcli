import os
from pathlib import Path
from shutil import copyfile
from src.command.command import Command


class CreateCommand(Command):
    def __init__(self, name):
        self.name = name

    def run(self, config):
        config_path = str(Path.home()) + "/.arkcli"
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        copyfile("conf/default.yaml", config_path + "/" + self.name + ".yaml")
