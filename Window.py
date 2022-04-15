import pygame, json, time

class Window:
    def __init__(self, width, height, title):
        self.__width = width
        self.__height = height
        self.__title = title
        self.__should_close = False

        self.__clock = pygame.time.Clock()

        self.__win = pygame.display.set_mode((self.__width, self.__height))
        self.__SURFACE = pygame.Surface((self.__width, self.__height))
        self.__block_data = self.__get_block_data()
        self.__block_images = {}
        pygame.display.set_caption(self.__title)

        self.__font = pygame.font.SysFont('freesansbold.ttf', 32)

        self.__add_every_block_img()

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_surface(self):
        return self.__SURFACE

    def __add_every_block_img(self):
        for i in self.__block_data["BLOCKS"]:
            img = self.__get_image_for_id(i["id"])
            self.__add_block_img(i["id"], img)

    def __add_block_img(self, id, img):
        self.__block_images[id] = img


    def __get_block_data(self):
        data = {}
        with open("Leveleditor/BlockData.json", "r") as file:
            data = json.loads(file.read())
            file.close()

        return data

    def __get_image_for_id(self, id:str):
        for e in self.__block_data["BLOCKS"]:
            if e["id"] == id:
                img_dir = e["image"]
                img = pygame.image.load(img_dir)
                return img


        return None

    def __get_every_block_id(self):
        lst = []
        for b in self.__block_data["BLOCKS"]:
            lst.append(b["id"])

        return lst


    def __update_entities(self, entities, player):
        keys = pygame.key.get_pressed()
        other_rects = []
        for entity in entities:
            if type(entity) != list:
                continue

            rect = None
            id = ""
            is_dead = False
            if len(entity) > 2:
                id = entity[2]
            if id != "SPAWN_POINT":
                if id not in self.__get_every_block_id():
                    is_other_player = False
                    if len(entity) > 4:
                        is_other_player = True

                    rect = pygame.Rect(entity[1], entity[2], 32, 32)

                    if is_other_player:
                        is_dead = entity[3]
                        name_text = self.__font.render(entity[0], True, (0, 0, 0), (255, 255, 255))
                        name_text_rect = name_text.get_rect(center=rect.center)
                        self.__SURFACE.blit(name_text, (name_text_rect[0], name_text_rect[1] - 30))
                        if len(entity) >= 6:
                            img = pygame.image.load(entity[5].replace(" ", ""))
                            if entity[6] == False:
                                img = pygame.transform.flip(img, True, False)
                            self.__SURFACE.blit(img, (entity[1], entity[2]))
                    else:
                        pygame.draw.rect(self.__SURFACE, (255, 0, 0), rect)
                else:
                    rect = pygame.Rect(entity[0], entity[1], 32, 32)
                    img = self.__block_images[entity[2]]
                    self.__SURFACE.blit(img, (entity[0], entity[1]))

            other_rects.append([rect, id, is_dead])

        player.update(self.__SURFACE, keys, other_rects)

    def update(self):
        pygame.display.update()

    def render_texts(self, texts, entities, player):
        self.__SURFACE.fill("white")
        if player != None:
            self.__update_entities(entities, player)
        for text in texts:
            self.__SURFACE.blit(text[0], (text[1], text[2]))

        self.__win.blit(self.__SURFACE, (0, 0))
        self.check_for_input()
        self.update()

        return self.__should_close

    def check_for_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__should_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__should_close = True

        return self.__should_close

    def loop(self, entities, player, texts):
        self.__SURFACE.fill("white")
        if player != None:
            self.__update_entities(entities, player)

        for text in texts:
            self.__SURFACE.blit(text[0], (text[1], text[2]))

        self.__win.blit(self.__SURFACE, (0, 0))
        self.update()
        self.check_for_input()
        self.__clock.tick(60)

        return self.__should_close
