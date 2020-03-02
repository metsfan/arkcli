from string import Template
from src.command.command import Command
from src.command.start import StartCommand
from src.command.stop import StopCommand
from src.helper.game_helper import GameHelper
from src.helper.steam_helper import SteamHelper
from src.helper.steamcmd_ex import SteamcmdEx


class UpdateCommand(Command):
    def __init__(self, only_if_needed, schedule):
        self.only_if_needed = only_if_needed
        self.schedule = schedule

    def run(self, server):
        config = server.config
        path = config['steamCmdPath']

        steamcmd = SteamcmdEx(path)

        if self.only_if_needed and \
                not SteamHelper.has_game_update(steamcmd, config, server.name):
            return

        running_pid = server.running_pid
        was_running = False

        if running_pid is not None:
            was_running = True
            StopCommand(schedule=self.schedule)\
                .run(server)

        print(Template('Updating game instance $name').substitute(
            name=server.name
        ))

        SteamHelper.install_game_and_mods(steamcmd, config, server.name)

        if was_running:
            StartCommand(stop_if_started=False, auto_restart=config["autoRestart"])\
                .run(server)
