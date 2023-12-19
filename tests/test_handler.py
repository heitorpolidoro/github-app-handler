import pytest

from githubapp import SignatureError
from githubapp.handlers.handler import Handler


def test_event_handler_method_validation():
    with pytest.raises(SignatureError) as err:
        Handler._validate_signature(lambda: None)

    expected_message = (
        "Method test_event_handler_method_validation.<locals>.<lambda>() "
        "signature error. The method must accept only one argument of the Event type"
    )
    assert str(err.value.message) == expected_message
