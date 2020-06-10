import os
from datetime import datetime
from logging import ERROR
from zipfile import ZipFile, ZIP_LZMA

from src.command.command import Command
from src.server_log import Level


class RestoreCommand(Command):
    def __init__(self, file):
        self.file = file

    def run(self, server):
        if server.running_pid is not None:
            server.log.append("Please stop the server before restoring", level=ERROR)
            return

        server.log.append("Restoring game data from " + self.file)
        config = server.config
        backup_file = config["gameBasePath"] + "/" + server.name + "/backup/" + self.file

        if not os.path.exists(backup_file):
            server.log.append("Backup " + self.file + " Not found", level=ERROR)
            return

        saved_dir = config["gameBasePath"] + "/" + server.name + "/ShooterGame/Saved"

        formatted_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        if os.path.exists(saved_dir + "/SavedArks"):
            os.rename(saved_dir + "/SavedArks", saved_dir + "/SavedArks.bak." + formatted_date)

        if os.path.exists(saved_dir + "/SaveGames"):
            os.rename(saved_dir + "/SaveGames", saved_dir + "/SaveGames.bak." + formatted_date)

        zipfile = ZipFile(backup_file, mode='r')
        zipfile.extractall(saved_dir)

        zipfile.close()
