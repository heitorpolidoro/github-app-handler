"""
Module for handling GitHub check_suite webhook events.
https://docs.github.com/en/webhooks/webhook-events-and-payloads#check_suite
"""
from github.CheckSuite import CheckSuite
from github.NamedUser import NamedUser
from github.Repository import Repository

from githubapp.events.event import Event
from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject


class CheckSuiteEvent(Event):
    """This class represents an check suite event."""

    event_identifier = {"event": "check_suite"}

    def __init__(
        self,
        headers,
        check_suite,
        repository,
        sender,
        **kwargs,
    ) -> None:
        super().__init__(headers, **kwargs)
        self.check_suite = LazyCompletableGithubObject.get_lazy_instance(
            CheckSuite, attributes=check_suite
        )
        self.repository = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=repository
        )
        self.sender = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=sender
        )


class CheckSuiteCompletedEvent(CheckSuiteEvent):
    """This class represents an check suite completed event."""

    event_identifier = {"action": "completed"}


class CheckSuiteRequestedEvent(CheckSuiteEvent):
    """This class represents an check suite requested event."""

    event_identifier = {"action": "requested"}


class CheckSuiteRerequestedEvent(CheckSuiteEvent):
    """This class represents an check suite rerequested event."""

    event_identifier = {"action": "rerequested"}
