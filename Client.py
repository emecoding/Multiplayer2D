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

    def __initialize(self, x, y, id):
        self.__player = Player(x, y)
        self.__window = Window(800, 600, f"Multiplayer 2D({id})")

    def connect(self):
        self.__client_socket.connect((self.__HOST, self.__PORT))
        print("Connected to the Server!")
        data = self.__client_socket.recv(1024).decode(TEXT_FORMAT)
        x = int(data.split(",")[0])
        y = int(data.split(",")[1])
        id = int(data.split(",")[2])
        self.__initialize(x, y, id)
        while self.__is_connected:
            self.__update()

        self.__client_socket.close()
        print("Closed connection to the server...")

    def get_size_of_list_as_bytes(self, lst:list):
        s = lst.__sizeof__()
        s = str(s).encode(TEXT_FORMAT)
        return s

    def __update(self):
        data, size = self.__player.getDataAsBytes()
        self.__client_socket.send(size)
        coming_data_size_message_was_succesfull = self.__client_socket.recv(1025).decode(TEXT_FORMAT)
        if coming_data_size_message_was_succesfull == MESSAGE_WAS_FAILED_TO_RECEIVE:
            self.__is_connected = False
        elif coming_data_size_message_was_succesfull == MESSAGE_WAS_SENT_SUCCESSFULLY:
            self.__client_socket.send(data)

        other_entities_size = self.__client_socket.recv(1024)
        if not other_entities_size:
            self.__client_socket.send(MESSAGE_WAS_FAILED_TO_RECEIVE.encode(TEXT_FORMAT))
            self.__is_connected = False
            return

        self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
        other_entities_size = int(other_entities_size.decode(TEXT_FORMAT))

        other_entities = pickle.loads(self.__client_socket.recv(other_entities_size))

        entities = []
        for entity in other_entities:
            entities.append([int(entity[0]), int(float(entity[1])), int(entity[2]), str(entity[3]), (255, 255, 0)])

        should_close, es = self.__window.loop(entities, self.__player)
        if should_close: self.__is_connected = False

        #size_of_es = self.get_size_of_list_as_bytes(es)

client = Client(PORT, HOST)
client.connect()