import os
from string import Template
from time import sleep

from src.command.command import Command
from src.command.rcon import RconCommand
from src.helper.game_helper import GameHelper
from psutil import Process, NoSuchProcess


class StopCommand(Command):
    def __init__(self, name, schedule):
        self.name = name
        self.schedule = schedule

    def run(self, config):
        if self.schedule is not None:
            minutes_left = self.schedule
            warning_command = "cheat broadcast Server will shut down in $minutes minutes for maintenance."
            while minutes_left > 0:
                print(str(minutes_left) + " until shutdown")
                warning_command_minutes = Template(warning_command).substitute(minutes=str(minutes_left))
                RconCommand(self.name, warning_command).run(config)
                minutes_left -= 1
                sleep(60)

        running_pid = GameHelper.running_pid(config, self.name)

        if running_pid is not None:
            print("Stopping game instance " + self.name + " with pid " + str(running_pid))

            try:
                proc = Process(running_pid)
                if proc is not None:
                    proc.terminate()
            except NoSuchProcess:
                print("Process " + str(running_pid) + " not found. This game instance is already stopped")

            os.unlink(GameHelper.pid_file_path(config, self.name))
        else:
            print("Game instance " + self.name + " is already stopped")
