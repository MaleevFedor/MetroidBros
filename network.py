import socket


class FakeNetwork:
        def __init__(self):
            self.player_id = 0
            self.player_positions = []

        def send_initial_positions(self, initial_positions):
            self.player_positions = initial_positions

        def exchange_player_info(self, player):
            return (self.player_positions)


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'localhost'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)