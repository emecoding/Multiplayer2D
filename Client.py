import socket, random, pickle
from Config import *
from Player import Player
from Window import Window


class Client:
    def __init__(self, PORT, HOST):
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__PORT = PORT
        self.__HOST = HOST

        self.__player: Player = None
        self.__window: Window = None
        self.__is_connected = True
        self.__map_entities = []

    def __initialize(self, x, y, id):
        self.__player = Player(x, y)
        self.__window = Window(800, 600, f"Multiplayer 2D({id})")

    def connect(self):
        self.__client_socket.connect((self.__HOST, self.__PORT))
        print("Connected to the Server!")
        data = self.__client_socket.recv(1024).decode(TEXT_FORMAT)
        splitted_data = data.split(",")
        x = int(splitted_data[0])
        y = int(splitted_data[1])
        id = int(splitted_data[2])

        self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
        size_of_map_entities = pickle.loads(self.__client_socket.recv(1024))
        self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
        self.__map_entities = pickle.loads(self.__client_socket.recv(int(size_of_map_entities)))

        self.__initialize(x, y, id)
        while self.__is_connected:
            self.__update()

        self.__client_socket.close()
        print("Closed connection to the server...")

    def __compine_two_lists(self, a, b):
        lst = []
        for i in a:
            lst.append(i)
        for i in b:
            lst.append(i)

        return lst

    def __update(self):
        data, size, msg = self.__player.getDataAsBytes()
        self.__client_socket.send(size)

        result = self.__client_socket.recv(1024)
        if not result:
            self.__is_connected = False
            return

        result = pickle.loads(result)
        if result == MESSAGE_WAS_SENT_SUCCESSFULLY:
            self.__client_socket.send(data)

        other_entities_size = self.__client_socket.recv(1024)
        if not other_entities_size:
            self.__is_connected = False
            return

        other_entities_size = pickle.loads(other_entities_size)

        self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
        s = 0
        if type(other_entities_size) != int:
            s = 1024
        else:
            s = other_entities_size

        other_entities = self.__client_socket.recv(s)
        if not other_entities:
            self.__is_connected = False
            return

        other_entities = pickle.loads(other_entities)
        self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))

        #---------------------------

        new_level_coming = self.__client_socket.recv(1024)
        if not new_level_coming:
            self.__is_connected = False
            return

        new_level_coming = pickle.loads(new_level_coming)
        #self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
        if new_level_coming == NEW_LEVEL_COMING_TRUE:
            self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
            pos = pickle.loads(self.__client_socket.recv(1024))
            self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))

            size_of_map_entities = pickle.loads(self.__client_socket.recv(1024))
            self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
            self.__map_entities = pickle.loads(self.__client_socket.recv(int(size_of_map_entities)))
            self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))

            self.__player.setPosition(pos[0], pos[1])
            self.__player.has_won = False

        should_close = self.__window.loop(self.__compine_two_lists(other_entities, self.__map_entities), self.__player)
        if should_close: self.__is_connected = False

client = Client(PORT, HOST)
client.connect()