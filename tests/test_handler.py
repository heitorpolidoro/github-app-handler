# from collections import defaultdict
# from unittest.mock import Mock
#
# import pytest
#
# from githubapp.Event import Event
# from githubapp.handlers.handler import Handler
#
import pytest

from githubapp.webhook_handler import SignatureError, WebhookHandler
from tests.mocks import EventTest, SubEventTest


def test_add_handler_sub_event(method):
    WebhookHandler.add_handler(SubEventTest, method)

    assert len(WebhookHandler.handlers) == 1
    assert WebhookHandler.handlers.get(SubEventTest) == [method]


def test_add_handler_event(method):
    WebhookHandler.add_handler(EventTest, method)

    assert len(WebhookHandler.handlers) == 1
    assert EventTest not in WebhookHandler.handlers
    assert WebhookHandler.handlers.get(SubEventTest) == [method]


def test_add_handler_event_and_sub_event(method):
    WebhookHandler.add_handler(EventTest, method)
    WebhookHandler.add_handler(SubEventTest, method)

    assert len(WebhookHandler.handlers) == 1
    assert EventTest not in WebhookHandler.handlers
    assert WebhookHandler.handlers.get(SubEventTest) == [method] * 2


def test_handle_sub_event(method, event_action_request):
    WebhookHandler.add_handler(SubEventTest, method)
    WebhookHandler.handle(*event_action_request)
    method.assert_called_once()
    assert isinstance(method.call_args_list[0].args[0], SubEventTest)


def test_handle_event(method, event_action_request):
    WebhookHandler.add_handler(EventTest, method)
    WebhookHandler.handle(*event_action_request)
    method.assert_called_once()
    assert isinstance(method.call_args_list[0].args[0], SubEventTest)


def test_handle_event_and_sub_event(method, event_action_request):
    WebhookHandler.add_handler(EventTest, method)
    WebhookHandler.add_handler(SubEventTest, method)
    WebhookHandler.handle(*event_action_request)
    assert method.call_count == 2
    assert all(isinstance(args, SubEventTest) for args in method.call_args_list[0].args)


def test_root():
    assert WebhookHandler.root("test")() == "test App up and running!"


def test_event_handler_method_validation():
    def method():
        return None

    with pytest.raises(SignatureError) as err:
        WebhookHandler._validate_signature(method)

    expected_message = (
        "Method test_event_handler_method_validation.<locals>.method() "
        "signature error. The method must accept only one argument of the Event type"
    )
    assert str(err.value.message) == expected_message


#
# class EventTest(Event):
#     name = "event"
#
#
# class SubEventTest(EventTest):
#     action = "action"
#
#
# class SubEvent2Test(EventTest):
#     pass
#
#
# class HandlerTest(Handler):
#     event = EventTest
#
#
# class SubHandlerTest(HandlerTest):
#     event = SubEventTest
#
#
# class SubHandler2Test(HandlerTest):
#     event = SubEvent2Test
#
#
# @pytest.fixture
# def handler_test():
#     return Mock(lambda e: None)
#
#
# @pytest.fixture(autouse=True)
# def setup_and_teardown():
#     yield
#     Handler.handlers = defaultdict(list)
#
#
# def test_add_handler(handler_test):
#     HandlerTest()(handler_test)
#
#     handlers = Handler.handlers
#     assert len(handlers) == 2
#     assert EventTest not in handlers
#     assert SubEventTest in handlers
#     assert SubEvent2Test in handlers
#     assert handlers[SubEventTest] == [handler_test]
#     assert handlers[SubEvent2Test] == [handler_test]
#
#
# def test_add_sub_handler(handler_test):
#     SubHandlerTest()(handler_test)
#
#     handlers = Handler.handlers
#     assert len(handlers) == 1
#     assert SubEventTest in handlers
#     assert handlers[SubEventTest] == [handler_test]
#
#
# def test_add_handler_and_sub_handler(handler_test):
#     HandlerTest()(handler_test)
#     SubHandlerTest()(handler_test)
#
#     handlers = Handler.handlers
#     assert len(handlers) == 2
#     assert SubEventTest in handlers
#     assert SubEvent2Test in handlers
#     assert handlers[SubEventTest] == [handler_test] * 2
#     assert handlers[SubEvent2Test] == [handler_test]
# # def test___call___to_any(handler_test):
# #     HandlerTest()(handler_test)
# #     SubHandlerTest()(handler_test)
# #
# #     handlers = Handler.handlers
# #     assert len(handlers) == 2
# #     assert SubEventTest in handlers
# #     assert SubEvent2Test in handlers
# #     assert handlers[SubEventTest] == [handler_test] * 2
# #     assert handlers[SubEvent2Test] == [handler_test]
#
#
# def test_call_handler(handler_test):
#     SubHandlerTest()(handler_test)
#     headers = {
#         "X-Github-Event": "event",
#         "X-Github-Hook-Id": 123,
#         "X-Github-Delivery": 123,
#         "X-Github-Hook-Installation-Target-Type": 123,
#         "X-Github-Hook-Installation-Target-Id": 123,
#     }
#     body = {
#         "action": "action",
#         "installation": {"id": 123},
#     }
#     Handler.handle(headers, body)
#
#     event = SubEventTest(headers=headers, **body)
#     handler_test.assert_called_once_with(event)
#
#
# # import pytest
# #
# # from githubapp import SignatureError
# # from githubapp.handlers.handler import Handler
# #
# #
# # def test_event_handler_method_validation():
# #     with pytest.raises(SignatureError) as err:
# #         Handler._validate_signature(lambda: None)
# #
# #     expected_message = (
# #         "Method test_event_handler_method_validation.<locals>.<lambda>() "
# #         "signature error. The method must accept only one argument of the Event type"
# #     )
# #     assert str(err.value.message) == expected_message
