from unittest.mock import Mock

import pytest
from github import UnknownObjectException

from githubapp import Config

CONFIG_TEST = """
config1: value1

config2:
    subconfig1: value2
    
config3:
    - value3
    - value4
"""


@pytest.fixture(autouse=True)
def clear_config():
    for attr in vars(Config).copy().keys():
        delattr(Config, attr)
    yield


def test_config():
    repository = Mock()
    repository.get_contents.return_value = Mock(decoded_content=CONFIG_TEST)
    Config.load_config_from_file("file", repository)

    assert Config.config1 == "value1"
    assert Config.config2.subconfig1 == "value2"
    assert Config.config3 == ["value3", "value4"]
    assert Config.config4 is None


def test_is_feature_enables():
    repository = Mock()
    repository.get_contents.return_value = Mock(
        decoded_content="""
feature1: True
feature2:
    attr: x
feature3: False
"""
    )
    Config.load_config_from_file("file", repository)

    assert Config.is_feature1_enabled
    assert Config.is_feature2_enabled
    assert not Config.is_feature3_enabled
    assert Config.is_feature4_enabled


def test_config_on_file_not_found():
    repository = Mock()
    repository.get_contents.side_effect = UnknownObjectException(404)
    Config.load_config_from_file("file", repository)

    assert Config.config1 is None
