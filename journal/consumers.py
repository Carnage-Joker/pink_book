from channels.generic.websocket import JsonWebsocketConsumer


class PointsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def update_points(self, event):
        self.send_json({
            "points": event["points"]
        })
