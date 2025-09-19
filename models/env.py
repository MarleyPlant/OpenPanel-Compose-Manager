import os


class ENVFile:
    def __init__(self, path):
        self.path = path
        self.env = {}
        self.loadEnv()

    @property
    def data(self):
        data = []
        for key in self.env:
            data.append(f"{key}={self.env[key]}")
        return data

    def loadEnv(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            key, value = line.split("=", 1)
                            self.env[key] = value
