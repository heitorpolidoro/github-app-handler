# import pytest
#
# from githubapp.events.event import Event
# from githubapp.events.issue_comment import (
#     IssueCommentCreatedEvent,
#     IssueCommentDeletedEvent,
#     IssueCommentEditedEvent,
# )
# from githubapp.handlers.handler import Handler
#
#
# def test_issue_comment_created(event_action_request):
#     headers, body = event_action_request
#     headers["X-Github-Event"] = "issue_comment"
#     body["action"] = "created"
#     event = Event.get_event(headers, body)
#     assert event == IssueCommentCreatedEvent
#     event(headers, **body)
#
#
# def test_issue_comment_edited(event_action_request):
#     headers, body = event_action_request
#     headers["X-Github-Event"] = "issue_comment"
#     body["action"] = "edited"
#     event = Event.get_event(headers, body)
#     assert event == IssueCommentEditedEvent
#     event(headers, **body)
#
#
# def test_issue_comment_deleted(event_action_request):
#     headers, body = event_action_request
#     headers["X-Github-Event"] = "issue_comment"
#     body["action"] = "deleted"
#     event = Event.get_event(headers, body)
#     assert event == IssueCommentDeletedEvent
#     event(headers, **body)
#
#
# #
# #
# # def test_issue_comment_deleted():
# #     event = event_factory(
# #         "issue_comment",
# #         "deleted",
# #         add_to_body=["issue", "repository", "sender", "comment"],
# #     )
# #     assert isinstance(event, IssueCommentDeletedEvent)
# #
# #
# # def test_issue_comment_edited():
# #     event = event_factory(
# #         "issue_comment",
# #         "edited",
# #         add_to_body=["issue", "repository", "sender", "comment", "changes"],
# #     )
# #     assert isinstance(event, IssueCommentEditedEvent)
