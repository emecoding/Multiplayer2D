from Level import *
import os

class Game:
    def __init__(self, id):
        self.id = id
        self.entities = []
        self.map_entities = []

        self.load_level("Leveleditor/Files/level1.json")

    def load_level(self, path):
        lst = load(path)
        for e in lst:
            self.map_entities.append(e)

    def get_entities_without_one_index(self, index):
        lst = []
        for i in range(len(self.entities)):
            if i != index:
                lst.append(self.entities[i])

        return lst

