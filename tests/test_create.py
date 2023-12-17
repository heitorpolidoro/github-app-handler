from github_app.CreateEvent import CreateEvent
from tests.factory import event_factory


def test_create():
    event = event_factory(
        "create",
        None,
        add_to_body=[
            "description",
            "master_branch",
            "pusher_type",
            "ref",
            "ref_type",
            "repository",
            "sender",
        ],
    )
    assert isinstance(event, CreateEvent)
