# from githubapp.events import CreateTagEvent
# from githubapp.events.event import Event
# from githubapp.events.release import ReleaseReleasedEvent, ReleaseCreatedEvent
#
#
# def test_release_released(event_action_request):
#     headers, body = event_action_request
#     headers["X-Github-Event"] = "release"
#     body["action"] = "released"
#
#     event = Event.get_event(headers, body)
#     assert event == ReleaseReleasedEvent
#     event(headers, **body)
#
#
# def test_release_created(event_action_request):
#     headers, body = event_action_request
#     headers["X-Github-Event"] = "release"
#     body["action"] = "created"
#
#     event = Event.get_event(headers, body)
#     assert event == ReleaseCreatedEvent
#     event(headers, **body)
#
#
# # from githubapp import ReleaseReleasedEvent
# # from githubapp.ReleaseEvent import ReleaseCreatedEvent
# # from tests.factory import event_factory
# #
# #
# # def test_release_released():
# #     event = event_factory(
# #         "release", "released", add_to_body=["release", "repository", "sender"]
# #     )
# #     assert isinstance(event, ReleaseReleasedEvent)
# #
# #
# # def test_release_created():
# #     event = event_factory(
# #         "release", "created", add_to_body=["release", "repository", "sender"]
# #     )
# #     assert isinstance(event, ReleaseCreatedEvent)
