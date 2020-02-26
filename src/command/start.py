import os
import time
from threading import Thread

from src.command.command import Command
from subprocess import Popen

from src.command.stop import StopCommand
from src.command.watch import WatchCommand
from src.helper.game_helper import GameHelper

from psutil import Process, NoSuchProcess


class StartCommand(Command):
    def __init__(self, name, stop_if_started, auto_restart):
        self.name = name
        self.stop_if_started = stop_if_started
        self.auto_restart = auto_restart

    def run(self, config):
        self.start_server(config)

    def start_server(self, config):
        game_path = GameHelper.game_path(config, self.name)
        if not os.path.exists(game_path):
            raise FileNotFoundError("Path not found for name " + self.name)

        if self.stop_if_started:
            StopCommand(self.name, schedule=None).run(config)
            # Give any active watcher time to quit
            time.sleep(1.5)
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

            Thread(target=self.start_watch, args=(proc.pid, config), daemon=True)\
                .start()

    def start_watch(self, pid, config):
        print("Started watcher on pid " + str(pid))

        while True:
            try:
                Process(pid)
                # print("pid " + str(pid) + " still running. All is well.")
                time.sleep(1)
            except NoSuchProcess:
                if GameHelper.running_pid(config, self.name) is not None:
                    # Pid file still exists, so this was not a graceful shutdown, so start it up again
                    # print("Unexpected shutdown detected. Restarting server.")
                    self.stop_if_started = True
                    self.start_server(config)

                break
