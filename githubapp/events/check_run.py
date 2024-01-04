"""
Module for handling GitHub check_run webhook events.
https://docs.github.com/en/webhooks/webhook-events-and-payloads#check_run
"""
from github.CheckRun import CheckRun
from github.NamedUser import NamedUser
from github.Repository import Repository

from githubapp.events.event import Event
from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject


class CheckRunEvent(Event):
    """This class represents an check run event."""

    event_identifier = {"event": "check_run"}

    def __init__(
        self,
        headers,
        check_run,
        repository,
        sender,
        **kwargs,
    ):
        super().__init__(headers, **kwargs)
        self.check_run = LazyCompletableGithubObject.get_lazy_instance(
            CheckRun, attributes=check_run
        )
        self.repository = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=repository
        )
        self.sender = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=sender
        )


class CheckRunCompletedEvent(CheckRunEvent):
    """This class represents an check run completed event."""

    event_identifier = {"action": "completed"}
