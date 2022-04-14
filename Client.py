import socket, random, pickle, time, sys

import pygame.font

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
        self.__name = self.__get_name()
        self.__texts = []
        self.__font = pygame.font.SysFont('freesansbold.ttf', 32)
        self.__deaths_text = None
        self.__timer_text = None

    def __get_name(self):
        return str(input("Type name: "))

    def __initialize(self, x, y, id):
        self.__player = Player(x, y)
        self.__window = Window(800, 600, f"Multiplayer 2D({id})({self.__name})")

        self.__deaths_text = self.__font.render(f"Deaths: {self.__player.get_deaths()}", True, (0, 0, 0), (255, 255, 255))
        self.__timer_text = self.__font.render(f"Time: {float(self.__player.getTime())}", True, (0, 0, 0),
                                                (255, 255, 255))


    def connect(self):
        self.__client_socket.connect((self.__HOST, self.__PORT))
        print("Connected to the Server!")
        data = self.__client_socket.recv(1024).decode(TEXT_FORMAT)
        splitted_data = data.split(",")
        x = int(splitted_data[0])
        y = int(splitted_data[1])
        id = int(splitted_data[2])
        required_connections = int(splitted_data[3])

        self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
        size_of_map_entities = pickle.loads(self.__client_socket.recv(1024))
        self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
        self.__map_entities = pickle.loads(self.__client_socket.recv(int(size_of_map_entities)))

        self.__client_socket.send(self.__name.encode(TEXT_FORMAT))

        self.__initialize(x, y, id)

        starting = GAME_NOT_STARTING_MESSAGE
        while starting == GAME_NOT_STARTING_MESSAGE:
            data = self.__client_socket.recv(1024)
            if not data:
                self.__is_connected = False
                break
            data = data.decode(TEXT_FORMAT)
            self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
            if len(self.__texts) == 0:
                text = self.__font.render("Waiting for players...", True, (0, 0, 0), (255, 255, 255))
                r = text.get_rect(center=pygame.Rect(0, 0, self.__window.get_width(), self.__window.get_height()).center)
                self.__texts.append([text, r[0], r[1], 3])
            if int(data) < required_connections:
                should_close = self.__window.render_texts(self.__texts, [], None)
                if should_close:
                    self.__is_connected = False
                    sys.exit()
            else:
                starting = GAME_STARTING_MESSAGE

        print("Starting...")

        self.__texts.clear()
        self.__texts.append([self.__deaths_text, 0, 30, 3])
        self.__texts.append([self.__deaths_text, 0, 0, 3])

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
        self.__texts[0] = [self.__font.render(f"Deaths: {self.__player.get_deaths()}", True, (0, 0, 0),
                                                (255, 255, 255)), self.__texts[0][1], self.__texts[0][2], 0]
        self.__texts[1] = [self.__font.render(f"Time: {float(self.__player.getTime())}", True, (0, 0, 0),
                                              (255, 255, 255)), self.__texts[1][1], self.__texts[1][2], 0]
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

        new_level_data = pickle.loads(new_level_coming)
        if new_level_data[0] == NEW_LEVEL_COMING_TRUE:
            self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
            pos = pickle.loads(self.__client_socket.recv(1024))
            self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))

            size_of_map_entities = pickle.loads(self.__client_socket.recv(1024))
            self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
            self.__map_entities = pickle.loads(self.__client_socket.recv(int(size_of_map_entities)))
            self.__client_socket.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))


            self.__texts.clear()
            text = self.__font.render(f"Winner Is {new_level_data[1]}", True, (0, 0, 0), (255, 255, 255))
            r = text.get_rect(center=pygame.Rect(0, 0, self.__window.get_width(), self.__window.get_height()).center)
            self.__texts.append([text, r[0], r[1], 3])

            level_name_text = self.__font.render(f"Next Level Is {new_level_data[2]}", True, (255, 0, 0), (255, 255, 255))
            self.__texts.append([level_name_text, r[0] - 30, r[1] + 50, 3])

            self.__window.render_texts(self.__texts, [], self.__player)
            time.sleep(3)
            self.__texts.clear()
            self.__texts.append([self.__deaths_text, 0, 30, 3])
            self.__texts.append([self.__deaths_text, 0, 0, 3])

            self.__player.setPosition(pos[0], pos[1])
            self.__player.has_won = False
            self.__player.reset_deaths()
            self.__player.start_timer()

        should_close = self.__window.loop(self.__compine_two_lists(other_entities, self.__map_entities), self.__player, self.__texts)
        if should_close: self.__is_connected = False

client = Client(PORT, HOST)
client.connect()