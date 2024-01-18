import yaml
from github import UnknownObjectException


class ConfigValue:
    def set_values(self, data):
        """ Set the attributes from a data dict """
        for attr, value in data.items():
            if isinstance(value, dict):
                config_value = ConfigValue()
                config_value.set_values(value)
                setattr(self, attr, config_value)
            else:
                setattr(self, attr, value)

    def load_config_from_file(self, filename, repository):
        """ Load the config from a file """
        try:
            raw_data = (
                yaml.safe_load(
                    repository.get_contents(
                        filename, ref=repository.default_branch
                    ).decoded_content
                )
                or {}
            )
            self.set_values(raw_data)
        except UnknownObjectException:
            pass

    def __getattr__(self, item):
        if item.startswith("is_") and item.endswith("_enabled"):
            return getattr(self, item[3:-8]) is not False
        return None


Config = ConfigValue()
