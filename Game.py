class Game:
    def __init__(self, id):
        self.id = id
        self.entities = []


    def get_entities_without_one_index(self, index):
        lst = []
        for i in range(len(self.entities)):
            if i != index:
                lst.append(self.entities[i])

        return lst

