from string import Template
from pysteamcmd import Steamcmd
from src.command.command import Command
from src.command.start import StartCommand
from src.command.stop import StopCommand
from src.helper.game_helper import GameHelper
from src.helper.steam_helper import SteamHelper


class UpdateCommand(Command):
    def __init__(self, name, only_if_needed, schedule):
        self.name = name
        self.only_if_needed = only_if_needed
        self.schedule = schedule

    def run(self, config):
        running_pid = GameHelper.running_pid(config, self.name)
        was_running = False

        if running_pid is not None:
            was_running = True
            StopCommand(self.name, schedule=self.schedule).run(config)

        path = config['steamCmdPath']
        steamcmd = Steamcmd(path)

        print(Template('Updating game instance $name').substitute(
            name=self.name
        ))

        SteamHelper.install_game_and_mods(steamcmd, config, self.name)

        if was_running:
            StartCommand(self.name, stop_if_started=False, auto_restart=config["autoRestart"]).run(config)
