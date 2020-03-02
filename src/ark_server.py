import time
import os

from pathlib import Path

from threading import Thread
from psutil import Popen, Process, NoSuchProcess
from string import Template

from src.config import Config
from src.helper.game_helper import GameHelper

from src.command.backup import BackupCommand
from src.command.cleanup import CleanupCommand
from src.command.create import CreateCommand
from src.command.installmods import InstallModsCommand
from src.command.rcon import RconCommand
from src.command.restore import RestoreCommand
from src.command.install import InstallCommand
from src.command.update import UpdateCommand
from src.command.start import StartCommand
from src.command.stop import StopCommand
from src.command.status import StatusCommand


class ArkServer:
    def __init__(self, name):
        self.name = name

        self.installing = False
        self.running_pid = None
        self._status = None
        self._active = True
        self.auto_restart = False

        config_path = str(Path.home()) + "/.arkcli/" + name + ".yaml"
        if os.path.exists(config_path):
            self.installed = True
            print("Loading config from " + config_path)
            self.config = Config(config_path)

            self.game_path = GameHelper.game_path(self.config, self.name)
            self.auto_restart = self.config["autoRestart"]
        else:
            self.installed = False
            self.config = None
            self.game_path = None

    def _run_command(self, command):
        command.run(self)

    def install(self):
        self._run_command(InstallCommand())

    def install_mods(self):
        self._run_command(InstallModsCommand())

    def start(self, stop_if_started=False, auto_restart=True):
        self._run_command(StartCommand(stop_if_started=stop_if_started, auto_restart=auto_restart))

    def stop(self, schedule=None):
        self._run_command(StopCommand(schedule=schedule).run(self))

    def restart(self, schedule=None):
        self._run_command(StartCommand(stop_if_started=True, auto_restart=self.auto_restart, schedule=schedule))

    def update(self, schedule=None):
        self._run_command(UpdateCommand(only_if_needed=False, schedule=schedule))

    def backup(self):
        self._run_command(BackupCommand())

    def restore(self, file):
        self._run_command(RestoreCommand(file))

    def rconcmd(self, command):
        self._run_command(RconCommand(command))

    def status(self):
        self._run_command(StatusCommand(self._status_callback))
        return self._status

    def update_if_needed(self):
        self._run_command(UpdateCommand(only_if_needed=True, schedule=30))

    def _status_callback(self, data):
        self._status = data






