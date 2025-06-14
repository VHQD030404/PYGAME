# game_event.py

class GameEvent:
    def __init__(self, name, **data):
        self.name = name      # Tên sự kiện: "change_level", "player_dead", v.v.
        self.data = data      # Dữ liệu kèm theo: {"index": 2}, {"reason": "hazard"},...

class EventQueue:
    def __init__(self):
        self.queue = []

    def push(self, event: GameEvent):
        self.queue.append(event)

    def get(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def clear(self):
        self.queue = []
