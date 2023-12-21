class EventDataParser:
    def __init__(self, delivery, event, hook_id, hook_installation_target_id, hook_installation_target_type, installation_id, raw_headers, raw_body):
        self.delivery = delivery
        self.event = event
        self.hook_id = hook_id
        self.hook_installation_target_id = hook_installation_target_id
        self.hook_installation_target_type = hook_installation_target_type
        self.installation_id = installation_id
        self._raw_headers = raw_headers
        self._raw_body = raw_body
