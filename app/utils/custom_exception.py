class RESERVATION_NOT_FOUND(Exception):
    def __init__(self, message="Not Found"):
        self.message = message
        super().__init__(self.message)

class MIMETYPE_NOT_SUPPORTED(Exception):
    def __init__(self, message="Unsupported Media Type"):
        self.message = message
        super().__init__(self.message)