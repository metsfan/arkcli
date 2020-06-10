import os
from string import Template
from time import sleep

from src.command.command import Command
from src.command.rcon import RconCommand
from src.helper.game_helper import GameHelper
from psutil import Process, NoSuchProcess

from src.server_status import ServerStatus


class StopCommand(Command):
    def __init__(self, schedule):
        self.schedule = schedule

    def run(self, server):
        config = server.config
        if self.schedule is not None:
            minutes_left = self.schedule
            warning_command = "cheat broadcast Server will shut down in $minutes minutes for maintenance."
            while minutes_left > 0:
                if server.running_pid is None:
                    # Server was somehow else stopped, so abort countdown
                    return

                server.log.append(str(minutes_left) + " until shutdown")
                warning_command_minutes = Template(warning_command).substitute(minutes=str(minutes_left))
                RconCommand(server.name, warning_command).run(config)
                minutes_left -= 1
                sleep(60)

        running_pid = server.running_pid

        if running_pid is not None:
            server.log.append("Stopping game instance " + server.name + " with pid " + str(running_pid))

            try:
                proc = Process(running_pid)
                if proc is not None:
                    proc.terminate()
            except NoSuchProcess:
                server.log.append("Process " + str(running_pid) + " not found. This game instance is already stopped")

            pidfile = GameHelper.pid_file_path(config, server.name)
            if os.path.exists(pidfile):
                os.unlink(pidfile)

            server.running_pid = None
            server.running_status = ServerStatus.OFFLINE
        else:
            server.log.append("Game instance " + server.name + " is already stopped")
