# import inspect
# import logging
# from collections import defaultdict
# from typing import Callable, Any, Optional
#
# from githubapp import SignatureError
# from githubapp.Event import Event
# from githubapp.handlers.handler_old import Handler
#
#
# class Webhook:
#     _webhooks = defaultdict(list)
#     event: Optional[type[Event]] = None
#
#     @classmethod
#     def __call__(cls, method):
#         event = cls.event
#         if event is None and cls != Webhook:
#             raise AttributeError(f"Event not set for webhook: {cls.__name__}")
#
#         Handler.register_handler(event, method)
#         return method
#
#     @classmethod
#     def get_webhook(cls, headers, body):
#         """Returns the webhook class for the event and action in webhook"""
#         event = headers["X-Github-Event"]
#         action = body.pop("action", None)
#         body = body or {}
#         clazz = None
#         event_classes = list(filter(lambda x: x.event.name == event, cls.__subclasses__()))
#         if len(event_classes) > 1:
#             raise ValueError(f"Multiple webhook classes for '{event}'")
#         if len(event_classes) == 1:
#             event_class = event_classes[0]
#             if action is None:
#                 clazz = event_class
#             else:
#                 action_classes = list(
#                     filter(lambda x: x.event.action == action, event_class.__subclasses__())
#                 )
#                 if len(action_classes) > 1:
#                     raise ValueError(f"Multiple webhook classes for '{event}.{action}'")
#                 if len(action_classes) == 1:
#                     clazz = action_classes[0]
#
#         if clazz:
#             if sub_type := getattr(clazz, "sub_type", None):
#                 sub_type_value = body.get(sub_type)
#                 for sub_type_class in clazz.__subclasses__():
#                     if getattr(sub_type_class, sub_type) == sub_type_value:
#                         clazz = sub_type_class
#                         break
#             return clazz
#         event_name = event
#         if action:
#             event_name += f".{action}"
#
#         logging.warning(f"No webhook class for '{event_name}'")
