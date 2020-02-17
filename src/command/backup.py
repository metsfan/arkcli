import os
from datetime import datetime
from zipfile import ZipFile, ZIP_LZMA

from src.command.command import Command


class BackupCommand(Command):
    def __init__(self, name):
        self.name = name

    def run(self, config):
        backup_dir = config["gameBasePath"] + "/" + self.name + "/backup"

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        formatted_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        backup_file_name = backup_dir + "/backup_" + self.name + "_" + formatted_date + ".zip"

        saved_arks_dir = config["gameBasePath"] + "/" + self.name + "/ShooterGame/Saved/SavedArks"
        save_games_dir = config["gameBasePath"] + "/" + self.name + "/ShooterGame/Saved/SaveGames"

        zipfile = ZipFile(backup_file_name, mode='w', compression=ZIP_LZMA)
        if os.path.exists(saved_arks_dir):
            self.write_files_recursive(zipfile, saved_arks_dir, "SavedArks")

        if os.path.exists(save_games_dir):
            self.write_files_recursive(zipfile, save_games_dir, "SaveGames")

        zipfile.close()

    def write_files_recursive(self, zipfile, os_dir, zip_dir):
        zipfile.write(os_dir, zip_dir)
        files = os.listdir(os_dir)
        for file in files:
            if os.path.isdir(os_dir + "/" + file):
                self.write_files_recursive(zipfile, os_dir + "/" + file, zip_dir + "/" + file)
            else:
                zipfile.write(os_dir + "/" + file, zip_dir + "/" + file)


