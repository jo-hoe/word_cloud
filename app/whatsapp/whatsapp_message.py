from datetime import datetime


class WhatsAppMessage:

    def __init__(self, timestamp: datetime, username: str, message: str):
        self.timestamp = timestamp
        self.username = username
        self.message = message
