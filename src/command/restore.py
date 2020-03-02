import os
from datetime import datetime
from zipfile import ZipFile, ZIP_LZMA

from src.command.command import Command


class RestoreCommand(Command):
    def __init__(self, file):
        self.file = file

    def run(self, server):
        config = server.config
        backup_file = config["gameBasePath"] + "/" + server.name + "/backup/" + self.file + ".zip"

        if not os.path.exists(backup_file):
            print("Backup not found")
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
