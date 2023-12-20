# import inspect
# from collections import defaultdict
# from typing import Callable, Any
#
# from githubapp import SignatureError
# from githubapp.Event import Event
#
#
# class Handler:
#     _handlers = defaultdict(list)
#
#     def __init__(self, name, *args, **kwargs):
#         self.name = name
#
#     def root(self):
#         return f"{self.name} App up and running!"
#
#     @classmethod
#     def handle_webhook(cls, headers, body):
#         event = Event.parse_event(headers, body)
#         for handler in cls._handlers[event.__class__]:
#             handler(event)
#
#     @classmethod
#     def register_handler(cls, event: type[Event], handler: Callable[[Any], Any]):
#         cls._validate_signature(handler)
#         if event is None:
#             event = Event
#         cls._handlers[event].append(handler)
#         for sub_event in event.__subclasses__():
#             cls.register_handler(sub_event, handler)
#
#     @staticmethod
#     def _validate_signature(func):
#         parameters = inspect.signature(func).parameters
#         try:
#             assert len(parameters) == 1
#         except AssertionError:
#             signature = ""
#             raise SignatureError(func, signature)
