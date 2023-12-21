# from collections import defaultdict
# from unittest.mock import Mock
#
# import pytest
#
# from githubapp.Event import Event
# from githubapp.webhook_handler.handlers.handler import Handler
#
from unittest.mock import Mock, patch

import pytest

from githubapp import webhook_handler
from githubapp.webhook_handler import handle, _validate_signature
from tests.mocks import EventTest, SubEventTest


def test_add_handler_sub_event(method):
    """
    Test the addition of a handler for a sub event.

    Args:
        method: The method to be added as a handler.

    Raises:
        AssertionError: If the number of handlers is not as expected or if the added handler is not associated with the correct sub event.

    Example:
        test_add_handler_sub_event(mock_method)
    """

    with patch(
        "githubapp.webhook_handler._validate_signature",
        return_value=True,
    ):
        webhook_handler.add_handler(SubEventTest, method)

    assert len(webhook_handler.handlers) == 1
    assert webhook_handler.handlers.get(SubEventTest) == [method]


def test_add_handler_event(method):
    """
    Add a handler for the specified method to the webhook handler.

    Args:
        method: The method to add as a handler.

    Raises:
        AssertionError: If the number of handlers is not 1, if EventTest is still in the handlers, or if the method is not added for SubEventTest.

    Example:
        test_add_handler_event(method)
    """

    webhook_handler.add_handler(EventTest, method)

    assert len(webhook_handler.handlers) == 1
    assert EventTest not in webhook_handler.handlers
    assert webhook_handler.handlers.get(SubEventTest) == [method]


def test_add_handler_event_and_sub_event(method):
    """
    Test adding event and sub-event handlers to the webhook handler.

    Args:
        method: The method to be added as a handler for the events.

    Raises:
        AssertionError: If the number of handlers is not as expected or if the event/sub-event is not added correctly.

    Example:
        test_add_handler_event_and_sub_event(method)
    """

    webhook_handler.add_handler(EventTest, method)
    webhook_handler.add_handler(SubEventTest, method)

    assert len(webhook_handler.handlers) == 1
    assert EventTest not in webhook_handler.handlers
    assert webhook_handler.handlers.get(SubEventTest) == [method] * 2


def test_handle_sub_event(method, event_action_request):
    """
    Test the handle_sub_event function.

    Args:
        method: The method to be tested.
        event_action_request: The event action request.

    Raises:
        AssertionError: If the method call count is not equal to 1.
        AssertionError: If the argument passed to the method is not an instance of SubEventTest.

    Example:
        test_handle_sub_event(method, event_action_request)
    """

    webhook_handler.add_handler(SubEventTest, method)
    handle(*event_action_request)
    method.assert_called_once()
    assert isinstance(method.call_args_list[0].args[0], SubEventTest)


def test_handle_event(method, event_action_request):
    """
    Test the handle_event function.

    Args:
        method: The method to be tested.
        event_action_request: The event action request.

    Raises:
        AssertionError: If the method call does not match the expected behavior.

    Example:
        test_handle_event(mock_method, event_action_request)
    """

    webhook_handler.add_handler(EventTest, method)
    handle(*event_action_request)
    method.assert_called_once()
    assert isinstance(method.call_args_list[0].args[0], SubEventTest)


def test_handle_event_and_sub_event(method, event_action_request):
    """
    Test the handle_event_and_sub_event function.

    Args:
    - method: The method to be tested.
    - event_action_request: The event action request to be tested.

    Raises:
    - AssertionError: If the method call count is not equal to 2 or if any argument in the method call args list is not an instance of SubEventTest.

    Example:
    test_handle_event_and_sub_event(method, event_action_request)
    """

    webhook_handler.add_handler(EventTest, method)
    webhook_handler.add_handler(SubEventTest, method)
    handle(*event_action_request)
    assert method.call_count == 2
    assert all(isinstance(args, SubEventTest) for args in method.call_args_list[0].args)


def test_root():
    """
    Test the root function of the webhook_handler.

    This function tests the root function of the webhook_handler by asserting that the result
    of calling the root function with the argument "test" is equal to "test App up and running!".

    Raises:
        AssertionError: If the result of calling the root function with the argument "test" is not equal to "test App up and running!".

    Example:
        test_root()
    """

    assert webhook_handler.root("test")() == "test App up and running!"


def test_event_handler_method_validation():
    """
    Test event handler method validation.

    This function tests the validation of an event handler method by checking if it raises a SignatureError
    when the method signature does not match the expected format.

    Raises:
        SignatureError: If the method signature does not match the expected format.

    Example:
        ```python
        def method():
            return None

        with pytest.raises(webhook_handler.SignatureError) as err:
            _validate_signature(method)

        expected_message = (
            "Method test_event_handler_method_validation.<locals>.method() "
            "signature error. The method must accept only one argument of the Event type"
        )
        assert str(err.value.message) == expected_message
        ```
    """

    def method():
        """
        This function does not take any arguments and returns None.

        Raises:
            No specific exceptions are raised.

        Example:
            The function can be called as follows:
            result = method()
        """

        return None

    with pytest.raises(webhook_handler.SignatureError) as err:
        _validate_signature(method)

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
#     Handler.webhook_handler.handlers = defaultdict(list)
#
#
# def test_add_handler(handler_test):
#     HandlerTest()(handler_test)
#
#     webhook_handler.handlers = Handler.webhook_handler.handlers
#     assert len(webhook_handler.handlers) == 2
#     assert EventTest not in webhook_handler.handlers
#     assert SubEventTest in webhook_handler.handlers
#     assert SubEvent2Test in webhook_handler.handlers
#     assert webhook_handler.handlers[SubEventTest] == [handler_test]
#     assert webhook_handler.handlers[SubEvent2Test] == [handler_test]
#
#
# def test_add_sub_handler(handler_test):
#     SubHandlerTest()(handler_test)
#
#     webhook_handler.handlers = Handler.webhook_handler.handlers
#     assert len(webhook_handler.handlers) == 1
#     assert SubEventTest in webhook_handler.handlers
#     assert webhook_handler.handlers[SubEventTest] == [handler_test]
#
#
# def test_add_handler_and_sub_handler(handler_test):
#     HandlerTest()(handler_test)
#     SubHandlerTest()(handler_test)
#
#     webhook_handler.handlers = Handler.webhook_handler.handlers
#     assert len(webhook_handler.handlers) == 2
#     assert SubEventTest in webhook_handler.handlers
#     assert SubEvent2Test in webhook_handler.handlers
#     assert webhook_handler.handlers[SubEventTest] == [handler_test] * 2
#     assert webhook_handler.handlers[SubEvent2Test] == [handler_test]
# # def test___call___to_any(handler_test):
# #     HandlerTest()(handler_test)
# #     SubHandlerTest()(handler_test)
# #
# #     webhook_handler.handlers = Handler.webhook_handler.handlers
# #     assert len(webhook_handler.handlers) == 2
# #     assert SubEventTest in webhook_handler.handlers
# #     assert SubEvent2Test in webhook_handler.handlers
# #     assert webhook_handler.handlers[SubEventTest] == [handler_test] * 2
# #     assert webhook_handler.handlers[SubEvent2Test] == [handler_test]
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
# # from githubapp.webhook_handler.handlers.handler import Handler
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
