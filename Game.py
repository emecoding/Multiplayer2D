from Level import *
import random


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

    def __remove_from_list(self, item, list):
        lst = []
        e = list
        e.remove(item)
        for i in e:
            lst.append(i)

        return lst

    def get_random_map_entities(self):
        random_map = random.choice(self.__maps)
        return self.get_map_entities(random_map)


    def get_map_entities(self, map=None):
        if map == None:
            map = self.__maps[self.__current_map]

        spawn_x = 0
        spawn_y = 0
        for i in map:
            if i[2] == "SPAWN_POINT":
                spawn_x = i[0] + (37 * len(self.entities))
                spawn_y = i[1]
                break

        name = map[-1]
        map.remove(map[-1])

        return map, [spawn_x, spawn_y], name

    def reset_map(self, name, map):
        for m in self.__maps:
            if map == m:
                m.append(name)
                break

        return map

    def __load_map(self, path):
        map, name = load(path)
        map.append(name)
        self.__maps.append(map)
        return map, name


    def get_entities_without_one_index(self, index):
        lst = []
        for i in range(len(self.entities)):
            if i != index:
                lst.append(self.entities[i])

        return lst

