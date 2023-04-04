from textwrap import dedent

class Admin():
    def __init__(self, server, client):
        self.elevated = True
        self.authenticated = False
        self.server = server
        self.client = client

    def start(self):
        self.outbound('Enter Password:')
        if self.inbound() == 'poster':
            self.authenticated = True
            self.loop()

    def loop(self):
        while self.elevated and self.authenticated:
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
        self.outbound('\nEnter Command:')

    def action_display(self):
        display = dedent(f"""
        Command [ param     : type      ]  - Descriptions
        __________________________________________________________________

        clients [ connected : switch    ]  - Shows all or connected clients
        players [ online    : switch    ]  - Shows all or online players
        quit    [                       ]  - Exit elevated admin panel

        """).strip('\n')
        self.outbound(display)

    def action_handler(self):
        action = self.inbound()
        if action == 'clients':
            self.outbound([client.address for client in self.server.connections])
        if action == 'players':
            self.outbound([client.game.player for client in self.server.connections])
        if action == 'quit':
            self.client.socket.close()

