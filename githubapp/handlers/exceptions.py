class SignatureError(Exception):
    def __init__(self, method, signature):
        self.message = f"Method {method.__qualname__}({signature}) signature error. The method must accept only one argument of the Event type"
