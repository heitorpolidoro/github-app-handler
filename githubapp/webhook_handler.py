from githubapp.events import Event
from githubapp.handlers import Handler


def webhook_handler(event: type[Event]):
    def decorator(method):
        Handler.add_handler(event, method)
        return method

    return decorator
