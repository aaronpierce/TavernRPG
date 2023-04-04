from .player import Player
from textwrap import dedent

class Game():
    def __init__(self, client):
        self.online = True
        self.client = client
        self.player = None

    def start(self):
        self.outbound('Enter your username:')
        self.player = Player(self, self.inbound())
        self.loop()

    def loop(self):
        while self.online and self.player.alive:
            self.prompt()
            self.action_handler()

    def inbound(self):
        message = self.client.get()
        if message:
            print(message)
        return message

    def outbound(self, message):
        self.client.send(message)

    def prompt(self):
        self.action_display()
        self.outbound(f'\n{self.player.name}@player > Choose action:')

    def action_display(self):
        display = dedent(f"""
        {self.player.name}
        -------------------
        a : Attack
        i : Invenotry
        -------------------
        """).strip('\n')
        self.outbound(display)

    def action_handler(self):
        action = self.inbound()
        if action == 'a':
            self.player.attack()
        if action == 'q':
            self.client.socket.close()

