from argparse import ArgumentParser
from pathlib import Path

from src.command.backup import BackupCommand
from src.command.cleanup import CleanupCommand
from src.command.create import CreateCommand
from src.command.rcon import RconCommand
from src.command.restore import RestoreCommand
from src.command.watch import WatchCommand
from src.config import Config
from src.command.install import InstallCommand
from src.command.update import UpdateCommand
from src.command.start import StartCommand
from src.command.stop import StopCommand

parser = ArgumentParser(description="Ark Server CLI Tools")
parser.add_argument('command', type=str, nargs=1, help="Command to run",
                    choices=['create',
                             'install',
                             'start',
                             'stop',
                             'restart',
                             'status',
                             'update',
                             'checkupdate',
                             'watch',
                             'rcon',
                             'backup',
                             'restore',
                             'cleanup'])

parser.add_argument('--pid', dest="pid")
parser.add_argument('--rconcmd', dest="rconcmd")
parser.add_argument('--file', dest="file")
parser.add_argument('--name', dest="name")
parser.add_argument('--warn', dest="name")
parser.add_argument('--schedule', dest="schedule")

args = parser.parse_args()

command = None
command_name = args.command[0]
instance_name = args.name or "main"

config_path = str(Path.home()) + "/.arkcli/" + instance_name + ".yaml"
print("Loading config from " + config_path)
config = Config(config_path)

if command_name == "create":
    command = CreateCommand(instance_name)
elif command_name == "install":
    command = InstallCommand(instance_name)
elif command_name == "update":
    command = UpdateCommand(instance_name, only_if_needed=False, schedule=args.schedule)
elif command_name == "checkupdate":
    command = UpdateCommand(instance_name, only_if_needed=True, schedule=args.schedule)
elif command_name == "start":
    command = StartCommand(instance_name, stop_if_started=False, auto_restart=config["autoRestart"])
elif command_name == "restart":
    command = StartCommand(instance_name, stop_if_started=True, auto_restart=config["autoRestart"])
elif command_name == "stop":
    command = StopCommand(instance_name, schedule=args.schedule)
elif command_name == 'watch':
    command = WatchCommand(instance_name, pid=int(args.pid))
elif command_name == "rcon":
    command = RconCommand(instance_name, command=args.rconcmd)
elif command_name == "backup":
    command = BackupCommand(instance_name)
elif command_name == "restore":
    command = RestoreCommand(instance_name, file=args.file)
elif command_name == "cleanup":
    command = CleanupCommand(instance_name)


if command is not None:
    command.run(config=config)


