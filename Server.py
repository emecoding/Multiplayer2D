import socket, threading, random
from Config import *
from Game import Game
import sys, pickle

class Server:
    def __init__(self, PORT, HOST):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__PORT = PORT
        self.__HOST = HOST

        self.__LOOKING_FOR_CONNECTIONS = True
        self.__MAX_CONNECTIONS = 4

        self.__GAMES = []

    def __threaded_client(self, conn:socket.socket, addr, game):
        x = random.randint(0, 600)
        y = 100
        id = len(game.entities)
        msg = f"{x},{y},{id}".encode(TEXT_FORMAT)
        conn.send(msg)
        is_connected = True

        data = [x, y]
        game.entities.append(data)
        my_index = len(game.entities) - 1

        while is_connected:
            coming_data_size = conn.recv(1024).decode(TEXT_FORMAT)
            if not coming_data_size:
                conn.send(MESSAGE_WAS_FAILED_TO_RECEIVE.encode(TEXT_FORMAT))
                is_connected = False
            else:
                conn.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
                coming_data = conn.recv(int(coming_data_size))
                if not coming_data:
                    is_connected = False

                coming_data = coming_data.decode(TEXT_FORMAT)
                if not coming_data:
                    is_connected = False
                else:
                    splitted_coming_data = coming_data.split(",")
                    if my_index > len(game.entities) - 1:
                        my_index = len(game.entities) - 1
                    game.entities[my_index] = [splitted_coming_data[0], splitted_coming_data[1]]
                    other_entities_lst = game.get_entities_without_one_index(my_index)

                    size_of_other_entities_lst = self.get_size_of_list_as_bytes(other_entities_lst)
                    other_entities_lst = pickle.dumps(other_entities_lst)

                    conn.send(size_of_other_entities_lst)
                    result = conn.recv(1024).decode(TEXT_FORMAT)
                    if result == MESSAGE_WAS_SENT_SUCCESSFULLY:
                        conn.send(other_entities_lst)




        conn.close()
        game.entities.remove(game.entities[my_index])
        print(f"Connection from {addr} closed...")

    def get_size_of_list_as_bytes(self, lst:list):
        s = lst.__sizeof__()
        s = str(s).encode(TEXT_FORMAT)
        return s

    def __generate_id(self, howLong):
        id = 0
        for i in range(howLong):
            id += random.randint(0, 1000)

        return id

    def __create_new_game(self):
        game = Game(self.__generate_id(10))
        self.__GAMES.append(game)

        return game

    def __get_game_without_every_player(self):
        for game in self.__GAMES:
            if len(game.entities) < self.__MAX_CONNECTIONS:
                return game

        return self.__create_new_game()

    def start(self):
        self.__server_socket.bind((self.__HOST, self.__PORT))
        self.__server_socket.listen()
        while self.__LOOKING_FOR_CONNECTIONS:
            conn, addr = self.__server_socket.accept()
            print(f"Connection from {addr}")

            game = None
            if len(self.__GAMES) == 0:
                game = self.__create_new_game()
            else:
                game = self.__get_game_without_every_player()

            thread = threading.Thread(target=self.__threaded_client, args=(conn, addr, game))
            thread.start()


server = Server(PORT, HOST)
server.start()