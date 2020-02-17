import os
from src.command.command import Command
from subprocess import Popen

from src.command.stop import StopCommand
from src.helper.game_helper import GameHelper

from psutil import Process, NoSuchProcess


class StartCommand(Command):
    def __init__(self, name, stop_if_started, auto_restart):
        self.name = name
        self.stop_if_started = stop_if_started
        self.auto_restart = auto_restart

    def run(self, config):
        game_path = GameHelper.game_path(config, self.name)
        if not os.path.exists(game_path):
            raise FileNotFoundError("Path not found for name " + self.name)

        if self.stop_if_started:
            StopCommand(self.name).run(config)
        else:
            if GameHelper.running_pid(config, self.name) is not None:
                print("Game instance " + self.name + " is already started")
                return

        print("Starting game instance " + self.name)

        start_cmd = game_path + "/" + config["startCommand"]

        proc = Popen(start_cmd)

        print("Started ark server with PID " + str(proc.pid))

        pidfile = open(game_path + "/running_pid", "w")
        pidfile.write(str(proc.pid))
        pidfile.close()

        if self.auto_restart:
            log_dir = config["serverLogPath"]
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            server_log = open(log_dir + "/ServerLog.txt", 'wb')
            Popen(["python", "main.py", "watch", "--pid", str(proc.pid)], stdout=server_log, stderr=server_log)

