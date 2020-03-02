from valve.source import NoResponseError

from src.command.command import Command
import requests
import valve.source.a2s
import valve.source.master_server

OFFLINE = 0
STARTING = 1
ONLINE = 2


class StatusCommand(Command):
    def __init__(self, callback):
        self.callback = callback

    def run(self, server):
        status = {
            "installed": server.installed,
            "installing": server.installing
        }

        if server.installed:
            status["running_pid"] = server.running_pid
            if server.running_pid is not None:
                ip = requests.get('https://checkip.amazonaws.com').text.strip()
                query_port = int(server.config["queryPort"])
                try:
                    with valve.source.a2s.ServerQuerier((ip, query_port)) as valve_server:
                        info = valve_server.info()
                        players = valve_server.players()

                        print("{player_count}/{max_players} {server_name}".format(**info))
                        status["server_status"] = ONLINE
                        status["server_info"] = {
                            "max_players": info.values["max_players"],
                            "player_count": info.values["player_count"],
                            "server_name": info.values["server_name"],
                            "map": info.values["map"]
                        }
                except NoResponseError:
                    status["server_status"] = STARTING
            else:
                status["server_status"] = OFFLINE

        self.callback(status)

