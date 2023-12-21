from githubapp import webhook_handler
from tests.mocks import SubEventTest, EventTest


def test_call_handler_sub_event(method, event_action_request):
    assert webhook_handler.webhook_handler(SubEventTest)(method) == method

    assert len(webhook_handler.handlers) == 1
    assert webhook_handler.handlers.get(SubEventTest) == [method]


