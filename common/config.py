import yaml
from os import path


class Config():
    __config__ = None

    def __init__(self, config_file="config_local.yaml") -> None:
        self.__config__ = self.init_config(config_file)

    def init_config(self, config_file):
        file_path = path.abspath(path.join(path.dirname(__file__), config_file))
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    def print_config(self):
        print(f'{self.__config__}')

    def get(self, key, section='general'):
        if section not in self.__config__:
            print(f'No "{section}" section found in configuration')
            return None

        if key not in self.__config__[section]:
            print(f'No "{key}" key in {section} section found in configuration')
            return None

        return self.__config__[section][key]
