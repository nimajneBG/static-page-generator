# TITLE
#
# NOTE: This file is *not* intended to be run on its own and won't do anything
#
# (c) by Benjamin Grau 2021

from os.path    import  join, isfile
from json       import  loads
from sys        import  exit

from exceptions import  InvalidTypeInConfigError, InvalidValueInConfigError


class Config():
    """Load and process the configuration file"""
    def __init__(self, filename: str, cwd: str):
        self.CONFIG_PATH = join(cwd, filename)
        self.FILENAME = filename

    def readConfig(self) -> None:
        """Load the config from the config file"""
        print(isfile(self.CONFIG_PATH))
        if isfile(self.CONFIG_PATH):
            with open(self.CONFIG_PATH) as f:
                config = f.read()
            self.CONFIG: dict = loads(config)
        else:
            raise FileNotFoundError(
                f'Config file at {self.CONFIG_PATH} not found. The location for '
            )

# Test
if __name__ == '__main__':
    from os import getcwd
    c = Config('config.jso', getcwd())
    c.readConfig()
    print(c.CONFIG)