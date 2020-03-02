import os
from string import Template
from src.command.command import Command
from src.helper.steam_helper import SteamHelper
from src.helper.steamcmd_ex import SteamcmdEx


class InstallModsCommand(Command):
    def run(self, server):
        config = server.config
        path = config['steamCmdPath']
        if not os.path.exists(path):
            raise FileNotFoundError("SteamCMD not installed. Please run install first")

        steamcmd = SteamcmdEx(path)

        print(Template('Installing mods for name $name').substitute(
            name=server.name
        ))

        SteamHelper.install_mods(steamcmd, config, server.name)
