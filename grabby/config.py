import yaml


class Config():
    __config__ = None

    def __init__(self) -> None:
        self.__config__ = self.init_config()

    def init_config(self):
        with open("config.yaml", "r") as f:
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


if __name__ == "__main__":
    config = Config()
    config.print_config()
    print(f'{config.get("debug")}')
    print(f'{config.get("username", "github")}')
