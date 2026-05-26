import datetime

class WebSocketMessage:
    def __init__(self, clientId: str, messageType: str, cookie: str):
        this.timestamp = datetime.datetime.now()
        this.clientId = clientId
        this.messageType = messageType
        this.cookie = cookie