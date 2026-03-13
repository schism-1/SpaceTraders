class SpaceTradersError(Exception):
    def __init__(self, message, code=None, data=None):
        super().__init__(message)
        self.code = code
        self.data = data

class TokenInvalidError(SpaceTradersError):
    """Raised when 401 unauthorised"""
    pass

class CooldownError(SpaceTradersError):
    """Raised when an action is attempted during ship cooldown"""
    def __init__(self, message, remaining_seconds):
        super().__init__(message)
        self.remaining_seconds = remaining_seconds