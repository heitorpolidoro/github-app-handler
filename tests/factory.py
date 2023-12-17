from github_app.Event import Event


def event_factory(event="event", action="action", add_to_body=None):
    """Factory to create events"""
    add_to_body = add_to_body or []
    body = {"action": action, "installation": {"id": 123}}
    for item in add_to_body:
        body.update({item: {}})
    return Event.parse_event(
        {
            "X-Github-Event": event,
            "X-Github-Hook-Id": 123,
            "X-Github-Delivery": 123,
            "X-Github-Hook-Installation-Target-Type": 123,
            "X-Github-Hook-Installation-Target-Id": 123,
        },
        body,
    )
