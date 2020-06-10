import os
from pathlib import Path
from shutil import copyfile
from src.command.command import Command


class CreateCommand(Command):
    def run(self, server):
        config_path = str(Path.home()) + "/.arkcli"
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        config_file = config_path + "/" + server.name + ".yaml"
        if not os.path.exists(config_file):
            server.log.append("Creating server config " + server.name + " at " + config_file)
            copyfile("conf/default.yaml", config_path + "/" + server.name + ".yaml")
