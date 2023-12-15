import json
import os

from github.GithubObject import CompletableGithubObject
from github.GitRelease import GitRelease
from github.Issue import Issue
from github.IssueComment import IssueComment
from github.NamedUser import NamedUser
from github.Repository import Repository

all_webhooks = {
    event.replace(".json", ""): {}
    for event in os.listdir("tests/webhooks")
    if event.endswith(".json")
}


def get_webhook_request(event, action=""):
    event_full_name = event
    if action:
        event_full_name = f"{event}.{action}"
    data = all_webhooks.get(event_full_name)
    if not data:
        with open(f"tests/webhooks/{event_full_name}.json") as f:
            data = json.load(f)
            all_webhooks[event_full_name] = data
    return data["headers"], data["data"]


def assert_event(event):
    for attr, value in event.__dict__.items():
        if issubclass(value.__class__, CompletableGithubObject):
            globals()[f"assert_{attr}"](value)


def assert_repository(repository):
    assert isinstance(repository, Repository)
    assert repository.id == 731794992
    assert repository.allow_auto_merge is True
    # assert list(repository.get_pulls())
    assert not list(repository.get_pulls())


def assert_issue(issue):
    assert isinstance(issue, Issue)
    assert issue.id == 2044399971
    assert len(list(issue.get_comments())) == 1


def assert_issue_comment(issue_comment):
    assert isinstance(issue_comment, IssueComment)
    assert issue_comment.id == 1858518602
    assert issue_comment.body == "Issue comment"
    assert not list(issue_comment.get_reactions())


def assert_named_user(named_user):
    assert isinstance(named_user, NamedUser)
    assert named_user.id == 14806300
    assert len(list(named_user.get_followers())) == 7


def assert_sender(sender):
    assert_named_user(sender)


def assert_release(release):
    assert isinstance(release, GitRelease)
    assert release.id == 134019540
    assert not list(release.get_assets())
