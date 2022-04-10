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
        is_connected = True
        x = random.randint(0, 600)
        y = 100
        id = len(game.entities)
        msg = f"{x},{y},{id}".encode(TEXT_FORMAT)
        conn.send(msg)
        conn.recv(1024)
        _, size_of_map_entities = self.get_size_of_list_as_bytes(game.map_entities)
        conn.send(pickle.dumps(size_of_map_entities))
        conn.recv(1024)
        conn.send(pickle.dumps(game.map_entities))

        data = [x, y]
        game.entities.append(data)
        my_index = len(game.entities) - 1

        while is_connected:
            coming_data_size = conn.recv(1024)
            if not coming_data_size:
                is_connected = False
                conn.send(MESSAGE_WAS_FAILED_TO_RECEIVE.encode(TEXT_FORMAT))
                break

            coming_data_size = int(coming_data_size.decode(TEXT_FORMAT))
            conn.send(MESSAGE_WAS_SENT_SUCCESSFULLY.encode(TEXT_FORMAT))
            coming_data = conn.recv(coming_data_size)
            if not coming_data:
                is_connected = False
                break

            coming_data = coming_data.decode(TEXT_FORMAT).split(",")

            if my_index >= len(game.entities):
                my_index = len(game.entities) - 1
            has_won = False
            if coming_data[2] == "True":
                has_won = True

            game.entities[my_index] = [int(coming_data[0]), int(coming_data[1]), has_won]

            other_entities = game.get_entities_without_one_index(my_index)
            _, size_of_other_entities = self.get_size_of_list_as_bytes(other_entities)


            conn.send(str(size_of_other_entities).encode(TEXT_FORMAT))
            result = conn.recv(1024)
            if not result:
                is_connected = False
                break

            result = result.decode(TEXT_FORMAT)
            if result == MESSAGE_WAS_SENT_SUCCESSFULLY:
                conn.send(pickle.dumps(other_entities))

            print(self.__check_for_wins(game))
            #self.__check_for_wins(game)

        conn.close()
        game.entities.remove(game.entities[my_index])
        print(f"Connection from {addr} closed...")

    def __check_for_wins(self, game):
        winners = 0
        for e in game.entities:
            if len(e) > 2:
                if e[2]:
                    winners += 1

        return winners == len(game.entities)



    def get_size_of_list_as_bytes(self, lst:list):
        s1 = lst.__sizeof__()
        s = str(s1).encode(TEXT_FORMAT)
        return s, len(pickle.dumps(lst))

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