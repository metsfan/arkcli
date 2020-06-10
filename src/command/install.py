import os
from string import Template
from src.command.command import Command
from src.helper.steam_helper import SteamHelper
from src.helper.steamcmd_ex import SteamcmdEx


class InstallCommand(Command):
    def run(self, server):
        server.installing = True
        config = server.config
        server.log.append("Installing steamCMD if needed")
        path = config['steamCmdPath']
        if not os.path.exists(path):
            os.makedirs(path)

        steamcmd = SteamcmdEx(path)
        if not os.path.isfile(steamcmd.steamcmd_exe):
            steamcmd.install()

        game_path = config["gameBasePath"] + "/" + server.name
        if not os.path.exists(game_path):
            os.makedirs(game_path)

        server.log.append(Template('Installing game instance $name at path $game_path').substitute(
            game_path=game_path,
            name=server.name
        ))

        SteamHelper.install_game_and_mods(steamcmd, config, server.name)

        server.installing = False
        server.installed = True
