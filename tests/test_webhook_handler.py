from githubapp.webhook_handler import webhook_handler
from tests.mocks import EventTest, SubEventTest


def test_call_handler_sub_event(method, event_action_request):
    """
    Test the call handler for sub event.

    Args:
        method: The method to be tested.
        event_action_request: The event action request.

    Raises:
        AssertionError: If the assertions fail.

    Example:
        test_call_handler_sub_event(method, event_action_request)
    """

    assert webhook_handler(SubEventTest)(method) == method

    assert len(handlers) == 1
    assert handlers.get(SubEventTest) == [method]
