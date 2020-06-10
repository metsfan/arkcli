import time
import os
from enum import Enum
from logging import ERROR

from pathlib import Path

from threading import Thread

import requests

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
from src.server_log import ServerLog, Level
from src.server_status import ServerStatus


class ArkServer:
    def __init__(self, name):
        self.name = name

        self.installing = False
        self.running_pid = None
        self._status = None
        self._active = True
        self.auto_restart = False
        self.log = ServerLog()

        self.ip = requests.get('https://checkip.amazonaws.com').text.strip()

        self.log.append("Server IP: " + self.ip)
        self.log.append("Now using " + name)

        self.running_status = ServerStatus.OFFLINE

        self.config_path = str(Path.home()) + "/.arkcli/" + name + ".yaml"
        if not os.path.exists(self.config_path):
            self._run_command(CreateCommand())

        self.installed = False
        self.config = None
        self.game_path = None

        self.reload_config()

    def _run_command(self, command):
        try:
            command.run(self)
        except Exception as e:
            self.log.append(str(e), Level.ERROR)

    def reload_config(self):
        self.log.append("Loading config from " + self.config_path)
        self.config = Config(self.config_path)

        game_path = GameHelper.game_path(self.config, self.name)
        if os.path.exists(game_path):
            self.installed = True
            self.game_path = game_path
            self.auto_restart = self.config["autoRestart"]

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

    def fetch_backups(self):
        backup_dir = self.config["gameBasePath"] + "/" + self.name + "/backup"
        return os.listdir(backup_dir)

    def cleanup(self):
        self._run_command(CleanupCommand())

    def _status_callback(self, data):
        self._status = data






