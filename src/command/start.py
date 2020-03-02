import os
import time
from threading import Thread

from src.command.command import Command
from subprocess import Popen

from src.command.stop import StopCommand
from src.helper.game_helper import GameHelper

from psutil import Process, NoSuchProcess


class StartCommand(Command):
    def __init__(self, stop_if_started, auto_restart, schedule=None):
        self.stop_if_started = stop_if_started
        self.auto_restart = auto_restart
        self.schedule = schedule

    def run(self, server):
        self.start_server(server)

    def start_server(self, server):
        config = server.config
        game_path = GameHelper.game_path(config, server.name)
        if not os.path.exists(game_path):
            raise FileNotFoundError("Path not found for name " + server.name)

        if self.stop_if_started:
            StopCommand(schedule=self.schedule).run(server)
            # Give any active watcher time to quit
            time.sleep(1.5)
        else:
            if server.running_pid is not None:
                print("Game instance " + server.name + " is already started")
                return

        print("Starting game instance " + server.name)

        start_cmd = game_path + "/" + config["startCommand"]

        proc = Popen(start_cmd)

        print("Started ark server with PID " + str(proc.pid))

        pidfile = open(game_path + "/running_pid", "w")
        pidfile.write(str(proc.pid))
        pidfile.close()

        server.running_pid = proc.pid

        if self.auto_restart:
            log_dir = config["serverLogPath"]
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            Thread(target=self.start_watch, args=(server,), daemon=True)\
                .start()

    def start_watch(self, server):
        while True:
            try:
                Process(server.running_pid)
                # print("pid " + str(pid) + " still running. All is well.")
                time.sleep(1)
            except NoSuchProcess:
                if server.running_pid is not None:
                    # Pid file still exists, so this was not a graceful shutdown, so start it up again
                    # print("Unexpected shutdown detected. Restarting server.")
                    self.stop_if_started = True
                    server.restart()

                break
