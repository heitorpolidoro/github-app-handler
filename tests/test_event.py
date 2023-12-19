import sys

import pytest

from githubapp.Event import Event
from tests.factory import event_factory


class EventTest(Event):
    name = "event"


class EventActionTest(EventTest):
    action = "action"


class EventDupTest(Event):
    name = "dup_event"


class EventDupTest2(Event):
    name = "dup_event"


class EventDupActionTest(EventTest):
    action = "dup_action"


class EventDupActionTest2(EventTest):
    action = "dup_action"



def test_parse_event():
    event_class = event_factory()
    assert isinstance(event_class, EventActionTest)


def test_parse_event_missing_action(caplog):
    Event.parse_event(
        {
            "X-Github-Event": "event",
        },
        {
            "action": "action2",
        },
    )
    assert "No webhook class for 'event.action2'" in caplog.text


def test_parse_event_missing_event(caplog):
    Event.parse_event(
        {
            "X-Github-Event": "event2",
        },
        {
            "action": "action",
        },
    )
    assert "No webhook class for 'event2.action'" in caplog.text


def test_validate_unique_event_name():
    with pytest.raises(ValueError) as err:
        Event.parse_event(
            {
                "X-Github-Event": "dup_event",
            },
            {
                "action": "action",
            },
        )
    assert str(err.value) == "Multiple webhook classes for 'dup_event'"


def test_validate_unique_action():
    with pytest.raises(ValueError) as err:
        Event.parse_event(
            {
                "X-Github-Event": "event",
            },
            {
                "action": "dup_action",
            },
        )
    assert str(err.value) == "Multiple webhook classes for 'event.dup_action'"
