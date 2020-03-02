import json
import time

from threading import Thread

from src.ark_server import ArkServer


class Api:
    def __init__(self):
        self.window = None
        self.server = None

        Thread(target=self._periodic_update_check, daemon=True).start()
        Thread(target=self._periodic_backup, daemon=True).start()

        Thread(target=self.periodic_sync, daemon=True).start()

    def init_window(self, window):
        self.window = window

    def useName(self, name):
        print("Using server name " + name)
        self.server = ArkServer(name)
        self.sync()

    def install(self):
        self.server.install()
        self.sync()

    def start(self):
        self.server.start()
        self.sync()

    def stop(self, with_warning, warning_minutes):
        schedule = None
        if with_warning:
            schedule = warning_minutes
        self.server.stop(schedule)
        self.sync()

    def restart(self, with_warning, warning_minutes):
        schedule = None
        if with_warning:
            schedule = warning_minutes
        self.server.restart(schedule)
        self.sync()

    def backup(self):
        self.server.backup()
        self.sync()

    def restore(self, file):
        self.server.restore(file)
        self.sync()

    def rconcmd(self, command):
        self.server.rconcmd(command)
        self.sync()

    def fetchBackups(self):
        print("reading backups")

    def sync(self):
        if self.server is not None:
            status = self.server.status()
            if status is not None:
                status_json = json.dumps(status)
                self.window.evaluate_js("sync(" + status_json + ")")

    def periodic_sync(self):
        while True:
            self.sync()
            time.sleep(0.016)

    def _periodic_update_check(self):
        while True:
            if self.server is not None and \
                    self.server.config is not None:
                update_check_minutes = int(self.server.config["updateCheckMinutes"])
                auto_update_schedule = int(self.server.config["autoUpdateWarnMinutes"])
                self.server.update(schedule=auto_update_schedule)
                time.sleep(update_check_minutes * 60)

    def _periodic_backup(self):
        while True:
            if self.server is not None and \
                    self.server.config is not None:
                backup_minutes = int(self.server.config["backupIntervalMinutes"])
                self.server.backup()
                time.sleep(backup_minutes * 60)
