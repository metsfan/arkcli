from Lib import subprocess
from pysteamcmd import Steamcmd, SteamcmdException


class SteamcmdEx(Steamcmd):
    def app_info_update(self, gameid, game_install_dir, user='anonymous', password=None):
        """
        Get the app info from the steam store
        :param gameid: steam game id for the files downloaded
        :param game_install_dir: installation directory for gameserver files
        :param user: steam username (defaults anonymous)
        :param password: steam password (defaults None)
        :return: subprocess call to steamcmd
        """

        steamcmd_params = (
            self.steamcmd_exe,
            '+login {} {}'.format(user, password),
            '+force_install_dir {}'.format(game_install_dir),
            '+app_info_update 1',
            '+app_info_print {}'.format(gameid),
            '+quit',
        )
        try:
            return subprocess.check_call(steamcmd_params)
        except subprocess.CalledProcessError:
            raise SteamcmdException("Steamcmd was unable to run. Did you install your 32-bit libraries?")