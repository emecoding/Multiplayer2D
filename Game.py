from Level import *


class Game:
    def __init__(self, id):
        self.id = id
        self.entities = []
        self.__maps = []
        self.__current_map = 0

        self.__map_1 = self.__load_map("Leveleditor/Files/level1.json")
        self.__map_2 = self.__load_map("Leveleditor/Files/level2.json")

    def current_map_index_plus(self):
        self.__current_map += 1
        if len(self.__maps) >= self.__current_map:
            self.__current_map = len(self.__maps) - 1
            return False

        return True

    def get_map_entities(self):
        spawn_x = 0
        spawn_y = 0
        for i in self.__maps[self.__current_map]:
            if i[2] == "SPAWN_POINT":
                spawn_x = i[0] + (37 * len(self.entities))
                spawn_y = i[1]
                break
        return self.__maps[self.__current_map], [spawn_x, spawn_y]

    def __load_map(self, path):
        map, name = load(path)
        self.__maps.append(map)
        return map, name


    def get_entities_without_one_index(self, index):
        lst = []
        for i in range(len(self.entities)):
            if i != index:
                lst.append(self.entities[i])

        return lst

