import os

from yaml import load, FullLoader


class Config:
    def __init__(self, file):
        if os.path.exists(file):
            fp = open(file, "r")
            content = fp.read()
            fp.close()
            self.data = load(content, Loader=FullLoader)

    def __getitem__(self, item):
        if item in self.data:
            return self.data[item]
        else:
            return None
