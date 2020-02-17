import os
from datetime import datetime
from zipfile import ZipFile, ZIP_LZMA
from shutil import rmtree

from src.command.command import Command


class CleanupCommand(Command):
    def __init__(self, name):
        self.name = name
        self.max_days = 10

    def run(self, config):
        saved_dir = config["gameBasePath"] + "/" + self.name + "/ShooterGame/Saved"
        if os.path.exists(saved_dir):
            files_list = os.listdir(saved_dir)
            for file in files_list:
                if "SavedArks.bak" in file or "SaveGames.bak" in file:
                    rmtree(saved_dir + "/" + file)

        backup_dir = config["gameBasePath"] + "/" + self.name + "/backup"
        if os.path.exists(backup_dir):
            files_list = os.listdir(backup_dir)
            now = datetime.now()

            for file in files_list:
                parts = file.split("_")
                file_date = datetime(int(parts[2]), int(parts[3]), int(parts[4]))
                time_diff = now - file_date
                if time_diff.days > self.max_days:
                    os.remove(backup_dir + "/" + file)
