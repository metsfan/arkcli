import os
from string import Template
from pysteamcmd import Steamcmd
from src.command.command import Command
from src.helper.steam_helper import SteamHelper


class InstallModsCommand(Command):
    def __init__(self, name):
        self.name = name

    def run(self, config):
        path = config['steamCmdPath']
        if not os.path.exists(path):
            raise FileNotFoundError("SteamCMD not installed. Please run install first")

        steamcmd = Steamcmd(path)

        print(Template('Installing mods for name $name').substitute(
            name=self.name
        ))

        SteamHelper.install_mods(steamcmd, config, self.name)
