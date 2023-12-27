import inspect

from githubapp.events.event import Event
from tests.conftest import event_action_request
from tests.mocks import EventTest, SubEventTest


def fill_body(body, *attributes):
    """
    Fill the body with specified attributes.

    Args:
        body (dict): The body to be filled.
        *attributes: Variable length argument list of attributes to be added to the body.

    Example:
        >>> body = {}
        >>> fill_body(body, "action", "release", "ref")
        >>> print(body)
        {'action': 'action', 'release': 'release', 'ref': 'ref'}
    """
    if isinstance(body, tuple):
        _, body = body
    for txt in [
        "action",
        "release",
        "master_branch",
        "pusher_type",
        "ref",
        "description",
        "comment",
    ]:
        if txt in attributes:
            body[txt] = txt
    for obj in ["repository", "sender", "issue", "changes"]:
        if obj in attributes:
            body[obj] = {}


# noinspection PyUnresolvedReferences
def test_init(event_action_request):
    headers, body = event_action_request
    SubEventTest(headers, **body)
    assert Event.github_event == "event"
    assert Event.hook_id == 1
    assert Event.delivery == "a1b2c3d4"
    assert Event.hook_installation_target_type == "type"
    assert Event.hook_installation_target_id == 2
    assert Event.installation_id == 3


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
        if subclasses := event_class.__subclasses__():
            for sub_event_class in subclasses:
                instantiate_class(body, headers, sub_event_class)
        else:
            instantiate_class(body, headers, event_class)


def instantiate_class(body, headers, clazz):
    """Instantiate and validate an event or sub event class"""
    body.update(clazz.event_identifier)
    event = Event.get_event(headers, body)
    assert event == clazz
    for attr in inspect.signature(event).parameters:
        if attr != "headers":
            body[attr] = "value"
    event(headers, **body)
