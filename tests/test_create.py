# import pytest
#
# from githubapp.events import CreateBranchEvent, CreateTagEvent
# from githubapp.events.event import Event
#
#
# def test_create_branch(event_action_request):
#     headers, body = event_action_request
#     headers["X-Github-Event"] = "create"
#     body["ref_type"] = "branch"
#     event = Event.get_event(headers, body)
#     assert event == CreateBranchEvent
#     event(headers, **body)
#
#
# def test_create_tag(event_action_request):
#     headers, body = event_action_request
#     headers["X-Github-Event"] = "create"
#     body["ref_type"] = "tag"
#     event = Event.get_event(headers, body)
#     assert event == CreateTagEvent
#     event(headers, **body)
#
#
# # from githubapp.events.create import CreateBranchEvent, CreateEvent, CreateTagEvent
# # from tests.factory import event_factory
# #
# #
# # def test_create():
# #     event = event_factory(
# #         "create",
# #         None,
# #         add_to_body=[
# #             "description",
# #             "master_branch",
# #             "pusher_type",
# #             "ref",
# #             "ref_type",
# #             "repository",
# #             "sender",
# #         ],
# #     )
# #     assert isinstance(event, CreateEvent)
# #
# #
# # def test_create_branch():
# #     event = event_factory(
# #         "create",
# #         None,
# #         extra={"ref_type": "branch"},
# #         add_to_body=[
# #             "description",
# #             "master_branch",
# #             "pusher_type",
# #             "ref",
# #             "ref_type",
# #             "repository",
# #             "sender",
# #         ],
# #     )
# #     assert isinstance(event, CreateBranchEvent)
# #
# #
# # def test_create_tag():
# #     event = event_factory(
# #         "create",
# #         None,
# #         extra={"ref_type": "tag"},
# #         add_to_body=[
# #             "description",
# #             "master_branch",
# #             "pusher_type",
# #             "ref",
# #             "ref_type",
# #             "repository",
# #             "sender",
# #         ],
# #     )
# #     assert isinstance(event, CreateTagEvent)
