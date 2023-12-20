from githubapp.events import *
# import pytest
#
# from githubapp.Event import Event
# from tests.factory import event_factory
#
from githubapp.events import Event
from tests.conftest import event_action_request
from tests.mocks import SubEventTest, EventTest


# noinspection PyUnresolvedReferences
def test_init(event_action_request):
    event = SubEventTest(*event_action_request)
    assert event.event == "event"
    assert event.hook_id == "1"
    assert event.delivery == "a1b2c3d4"
    assert event.hook_installation_target_type == "type"
    assert event.hook_installation_target_id == "3"
    assert event.action == "action"
    assert event.installation["id"] == "4"


def test_normalize_dicts():
    d1 = {"a": "1"}
    d2 = {"X-Github-batata": "Batata"}

    union_dict = Event.normalize_dicts(d1, d2)
    assert union_dict == {"a": "1", "batata": "Batata"}


def test_get_event(event_action_request):
    headers, body = event_action_request
    assert Event.get_event(headers, body) == SubEventTest
    body.pop("action")
    assert Event.get_event(headers, body) == EventTest


def test_match():
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 2}
    d3 = {"a": 1, "b": 1}

    class LocalEventTest(Event):
        pass

    LocalEventTest.event_identifier = d2
    assert LocalEventTest.match({}, d1) is True
    assert LocalEventTest.match({}, d3) is False
    LocalEventTest.event_identifier = d1
    assert LocalEventTest.match({}, d3) is False


def test_all_events(event_action_request):
    headers, body = event_action_request
    for event_class in Event.__subclasses__():
        if event_class.__name__.endswith("Test"):
            continue
        headers["X-Github-Event"] = event_class.event_identifier["event"]
        for sub_event_class in event_class.__subclasses__():
            body.update(sub_event_class.event_identifier)
            event = Event.get_event(headers, body)
            assert event == sub_event_class
            event(headers, **body)

# class EventTest(Event):
#     name = "event"
#
#
# class EventActionTest(EventTest):
#     action = "action"
#
#
# class EventDupTest(Event):
#     name = "dup_event"
#
#
# class EventDupTest2(Event):
#     name = "dup_event"
#
#
# class EventDupActionTest(EventTest):
#     action = "dup_action"
#
#
# class EventDupActionTest2(EventTest):
#     action = "dup_action"
#
#
# def test_parse_event():
#     event_class = event_factory()
#     assert isinstance(event_class, EventActionTest)
#
#
# def test_parse_event_missing_action(caplog):
#     Event.parse_event(
#         {
#             "Event": "event",
#         },
#         {
#             "action": "action2",
#         },
#     )
#     assert "No webhook class for 'event.action2'" in caplog.text
#
#
# def test_parse_event_missing_event(caplog):
#     Event.parse_event(
#         {
#             "Event": "event2",
#         },
#         {
#             "action": "action",
#         },
#     )
#     assert "No webhook class for 'event2.action'" in caplog.text
#
#
# def test_parse_event_missing_event_without_action(caplog):
#     Event.parse_event(
#         {
#             "Event": "event2",
#         },
#         {},
#     )
#     assert "No webhook class for 'event2'" in caplog.text
#
#
# def test_validate_unique_event_name():
#     with pytest.raises(ValueError) as err:
#         Event.parse_event(
#             {
#                 "Event": "dup_event",
#             },
#             {
#                 "action": "action",
#             },
#         )
#     assert str(err.value) == "Multiple webhook classes for 'dup_event'"
#
#
# def test_validate_unique_action():
#     with pytest.raises(ValueError) as err:
#         Event.parse_event(
#             {
#                 "Event": "event",
#             },
#             {
#                 "action": "dup_action",
#             },
#         )
#     assert str(err.value) == "Multiple webhook classes for 'event.dup_action'"
