from enum import Enum


class Level(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3


class ServerLog:
    def __init__(self):
        self.logs = []

    def clear(self):
        self.logs = []

    def fetch(self):
        return self.logs

    def append(self, text, level=Level.INFO):
        self.logs.append({"level": level.value, "data": text})

