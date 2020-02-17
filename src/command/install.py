import os
from string import Template
from pysteamcmd import Steamcmd
from src.command.command import Command
from src.helper.steam_helper import SteamHelper


class InstallCommand(Command):
    def __init__(self, name):
        self.name = name

    def run(self, config):
        print("Installing steamCMD if needed")
        path = config['steamCmdPath']
        if not os.path.exists(path):
            os.makedirs(path)

        steamcmd = Steamcmd(path)
        if not os.path.isfile(steamcmd.steamcmd_exe):
            steamcmd.install()

        game_path = os.path.join(config["gameBasePath"], self.name)
        if not os.path.exists(game_path):
            os.makedirs(game_path)

        print(Template('Installing game instance $name at path $game_path').substitute(
            game_path=game_path,
            name=self.name
        ))

        SteamHelper.install_game_and_mods(steamcmd, config, self.name)
