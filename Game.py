from Level import *
import os

class Game:
    def __init__(self, id):
        self.id = id
        self.entities = []
        self.__maps = []
        self.__current_map = 0

        self.__map_1 = self.__load_map("Leveleditor/Files/level1.json")
        self.__map_2 = self.__load_map("Leveleditor/Files/level1.json")

    def current_map_index_plus(self):
        self.__current_map += 1

    def get_map_entities(self):
        if len(self.__maps) >= self.__current_map:
            self.__current_map = len(self.__maps) - 1
        return self.__maps[self.__current_map]

    def __load_map(self, path):
        map = load(path)
        self.__maps.append(map)
        return map


    def get_entities_without_one_index(self, index):
        lst = []
        for i in range(len(self.entities)):
            if i != index:
                lst.append(self.entities[i])

        return lst

