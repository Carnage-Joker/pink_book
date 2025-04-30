from channels.generic.websocket import JsonWebsocketConsumer


class PointsConsumer(JsonWebsocketConsumer):

    def connect(self):
        if self.scope["user"].is_authenticated:
            self.accept()
        else:
            self.close(code=4001)  # Custom error for unauthenticated WebSocket
    def disconnect(self, close_code):
        pass

    def update_points(self, event):
        self.send_json({
            "points": event["points"]
        })
