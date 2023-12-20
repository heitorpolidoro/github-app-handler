#
# from githubapp import ReleaseEvent
# from githubapp.Event import Event
#
#


#     event = None
#
#     @classmethod
#     def __call__(cls, handler):
#         if sub_handlers := cls.__subclasses__():
#             for sub_handler in sub_handlers:
#                 sub_handler()(handler)
#         else:
#             cls.handlers[cls.event].append(handler)
#
#     @classmethod
#     def handle(cls, headers, body):
#         if event := Event.get_event(headers, body):
#             for handler in cls.handlers[event.__class__]:
#                 handler(event)
#
#
#
# class ReleaseHandler(Handler):
#     event = ReleaseEvent
#
