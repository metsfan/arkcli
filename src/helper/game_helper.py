import os
from platform import system


class GameHelper:
    @staticmethod
    def game_path(config, name):
        platform_type = system()

        platform_name = ""
        if platform_type == "Windows":
            platform_name = "Win64"
        elif platform_type == "Linux":
            platform_name = "Linux"

        return config["gameBasePath"] + "/" + name + "/ShooterGame/Binaries/" + platform_name

    @staticmethod
    def pid_file_path(config, name):
        return GameHelper.game_path(config, name) + "/running_pid"

    @staticmethod
    def running_pid(config, name):
        file_path = GameHelper.pid_file_path(config, name)
        if os.path.exists(file_path):
            pidfile = open(file_path, "r")
            pid = pidfile.readline()
            return int(pid)
        else:
            return None
