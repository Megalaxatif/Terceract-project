class Test():
    def __init__(self, game_context):
        super().__init__()
        self.game_context = game_context
        self.timer = 0
        self.name = "test"

    def update(self):
        self.timer += 1
        print("Test mini-game", self.timer)

