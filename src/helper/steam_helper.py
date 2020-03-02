import os

from src.helper.game_helper import GameHelper

AppId = 376030


class SteamHelper:
    @staticmethod
    def has_game_update(steamcmd, config, name):
        game_path = os.path.join(config["gameBasePath"], name)
        app_info = steamcmd.app_info_update(
            gameid=AppId,
            game_install_dir=game_path,
            user='anonymous',
            password=None
        )

        store_version = int(app_info.buildid)
        game_version = GameHelper.current_game_version(config, name)

        return store_version != game_version

    @staticmethod
    def install_game_and_mods(steamcmd, config, name):
        game_path = os.path.join(config["gameBasePath"], name)

        steamcmd.install_gamefiles(
            gameid=AppId,
            game_install_dir=game_path,
            user='anonymous',
            password=None,
            validate=True
        )

        SteamHelper.install_mods(steamcmd, config, name)

        app_info = steamcmd.app_info_update(
            gameid=AppId,
            game_install_dir=game_path,
            user='anonymous',
            password=None
        )

        store_version = int(app_info.buildid)
        GameHelper.write_game_version(config, name, store_version)

    @staticmethod
    def install_mods(steamcmd, config, name):
        game_path = os.path.join(config["gameBasePath"], name)
        mods = config["modIds"]

        if mods is not None:
            for mod in mods:
                steamcmd.install_workshopfiles(
                    gameid=AppId,
                    workshop_id=mod,
                    game_install_dir=game_path,
                    user='anonymous',
                    password=None,
                    validate=True
                )