class SignatureError(Exception):
    """Exception when the method has a wrong signature"""

    def __init__(self, method, signature):
        self.message = (
            f"Method {method.__qualname__}({signature}) signature error. "
            f"The method must accept only one argument of the Event type"
        )
