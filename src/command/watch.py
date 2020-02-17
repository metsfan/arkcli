import time
import os
from src.command.command import Command
from subprocess import Popen
from psutil import Process, NoSuchProcess

from src.helper.game_helper import GameHelper


class WatchCommand(Command):
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid

    def run(self, config):
        print("Started watcher on pid " + str(self.pid))

        while True:
            try:
                Process(self.pid)

                print("pid " + str(self.pid) + " still running. All is well.")

                time.sleep(5)
            except NoSuchProcess:
                if GameHelper.running_pid(config, self.name) is not None:
                    # Pid file still exists, so this was not a graceful shutdown, so start it up again
                    print("Unexpected shutdown detected. Restarting server.")
                    devnull = open(os.devnull, 'wb')
                    Popen(["python", "main.py", "restart"], stdout=devnull, stderr=devnull)
                else:
                    print("Ending watcher, process was stopped normally")

                break


