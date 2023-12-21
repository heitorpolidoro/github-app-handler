from githubapp.webhook_handler import webhook_handler
from tests.mocks import SubEventTest, EventTest


def test_call_handler_sub_event(method, event_action_request):
    assert webhook_handler(SubEventTest)(method) == method

    assert len(handlers) == 1
    assert handlers.get(SubEventTest) == [method]


