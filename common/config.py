import yaml
import re
import os
from os import path


class Config():
    __config__ = None
    path_matcher = re.compile(r'\$\{([^}^{]+)\}')

    def __init__(self, config_file="config_local.yaml") -> None:
        self.__config__ = self.init_config(config_file)

    def init_config(self, config_file):
        file_path = path.abspath(path.join(path.dirname(__file__), config_file))

        yaml.add_implicit_resolver('!path', self.path_matcher, None, yaml.SafeLoader)
        yaml.add_constructor('!path', self.path_constructor, yaml.SafeLoader)

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

    def path_constructor(self, loader, node):
        value = node.value
        match = self.path_matcher.match(value)
        env_var = match.group()[2:-1]
        return os.environ.get(env_var) + value[match.end():]
