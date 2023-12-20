# from githubapp.Event import Event
# from githubapp.webhooks import Webhook
#
#
# def event_factory(event="event", action="action", extra=None, add_to_body=None):
#     """Factory to create events"""
#     add_to_body = add_to_body or []
#     extra = extra or {}
#     body = {"installation": {"id": 123}}
#     if action:
#         body["action"] = action
#     for item in add_to_body:
#         body.update({item: {}})
#     if extra:
#         body.update(extra)
#     webhook = Webhook.get_webhook(
#         {
#             "X-Github-Event": event,
#             "X-Github-Hook-Id": 123,
#             "X-Github-Delivery": 123,
#             "X-Github-Hook-Installation-Target-Type": 123,
#             "X-Github-Hook-Installation-Target-Id": 123,
#         },
#         body,
#     )
#     if webhook:
#         return webhook.event
