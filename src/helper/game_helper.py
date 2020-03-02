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

    @staticmethod
    def version_file_path(config, name):
        return GameHelper.game_path(config, name) + "/version"

    @staticmethod
    def current_game_version(config, name):
        file_path = GameHelper.version_file_path(config, name)
        if os.path.exists(file_path):
            version_file = open(file_path, "r")
            version = version_file.readline()
            return int(version)
        else:
            return None

    @staticmethod
    def write_game_version(config, name, version):
        file_path = GameHelper.version_file_path(config, name)
        if os.path.exists(file_path):
            version_file = open(file_path, "w")
            version_file.write(version)
            version_file.close()
        else:
            return None
