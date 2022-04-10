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
        map_entities, spawn_pos = game.get_map_entities()
        is_connected = True
        id = len(game.entities)
        msg = f"{spawn_pos[0]},{spawn_pos[1]},{id}".encode(TEXT_FORMAT)
        conn.send(msg)
        conn.recv(1024)
        _, size_of_map_entities = self.get_size_of_list_as_bytes(map_entities)
        conn.send(pickle.dumps(size_of_map_entities))
        conn.recv(1024)
        conn.send(pickle.dumps(map_entities))

        data = [spawn_pos[0], spawn_pos[1]]
        game.entities.append(data)
        my_index = len(game.entities) - 1

        while is_connected:
            coming_data_size = conn.recv(1024)
            if not coming_data_size:
                is_connected = False
                break

            coming_data_size = int(coming_data_size.decode(TEXT_FORMAT))
            conn.send(pickle.dumps(MESSAGE_WAS_SENT_SUCCESSFULLY))
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
            conn.send(pickle.dumps(size_of_other_entities))
            result = conn.recv(1024)
            if not result:
                is_connected = False
                break

            result = result.decode(TEXT_FORMAT)
            if result == MESSAGE_WAS_SENT_SUCCESSFULLY:
                conn.send(pickle.dumps(other_entities))

            conn.recv(1024)

            won = self.__check_for_wins(game)

            if won:
                game.current_map_index_plus()
                map_entities, spawn_pos = game.get_map_entities()
                conn.send(pickle.dumps(NEW_LEVEL_COMING_TRUE))
                result = conn.recv(1024)
                conn.send(pickle.dumps(spawn_pos))
                conn.recv(1024)
                _, size_of_map_entities = self.get_size_of_list_as_bytes(map_entities)
                conn.send(pickle.dumps(size_of_map_entities))
                conn.recv(1024)
                conn.send(pickle.dumps(map_entities))
                conn.recv(1024)
            else:
                conn.send(pickle.dumps(NEW_LEVEL_COMING_FALSE))


        conn.close()
        game.entities.remove(game.entities[my_index])
        if len(game.entities) == 0:
            self.__GAMES.remove(game)
            print(f"Removed a game with id {game.id}")
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