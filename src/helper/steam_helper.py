import os


class SteamHelper:
    @staticmethod
    def install_game_and_mods(steamcmd, config, name):
        game_path = os.path.join(config["gameBasePath"], name)

        steamcmd.install_gamefiles(
            gameid=376030,
            game_install_dir=game_path,
            user='anonymous',
            password=None,
            validate=True
        )

        SteamHelper.install_mods(steamcmd, config, name)

    @staticmethod
    def install_mods(steamcmd, config, name):
        game_path = os.path.join(config["gameBasePath"], name)
        mods = config["modIds"]

        if mods is not None:
            for mod in mods:
                steamcmd.install_workshopfiles(
                    gameid=376030,
                    workshop_id=mod,
                    game_install_dir=game_path,
                    user='anonymous',
                    password=None,
                    validate=True
                )