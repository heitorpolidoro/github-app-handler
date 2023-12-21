from .event import Event


class EventMatcher:
    @classmethod
    def match(cls, *dicts):
        union_dict = Event.normalize_dicts(*dicts)
        for attr, value in cls.event_identifier.items():
            if not (attr in union_dict and value == union_dict[attr]):
                return False
        return True
