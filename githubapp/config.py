"""
Config module

This module handles loading configuration values from a YAML file
and provides access to those values via the ConfigValue class.
"""
from typing import Any

import yaml
from github import UnknownObjectException
from github.Repository import Repository


class ConfigError(AttributeError):
    pass


class ConfigValue:
    """The configuration loaded from the config file"""

    def __init__(self, value: Any = None) -> None:
        self._value = value

    def set_values(self, data: dict[str, Any]) -> None:
        """Set the attributes from a data dict"""
        for attr, value in data.items():
            if isinstance(value, dict):
                config_value = ConfigValue()
                config_value.set_values(value)
                setattr(self, attr, config_value)
            else:
                setattr(self, attr, value)

    def create_config(self, name, *, default=None, **values):
        if default is not None and values:
            raise ConfigError(
                "You cannot set the default value AND default values for sub values"
            )
        default = default or ConfigValue()
        self.set_values({name: default})
        if values:
            default.set_values(values)
        return getattr(self, name)

    def load_config_from_file(self, filename: str, repository: Repository) -> None:
        """Load the config from a file"""
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

    def __getattr__(self, item: str) -> Any:
        raise ConfigError(
            f"No such config value: {item}. And there is no default value for it"
        )


Config = ConfigValue()
