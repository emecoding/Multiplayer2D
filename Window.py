import pygame

class Window:
    def __init__(self, width, height, title):
        self.__width = width
        self.__height = height
        self.__title = title
        self.__should_close = False

        self.__clock = pygame.time.Clock()

        self.__win = pygame.display.set_mode((self.__width, self.__height))
        self.__SURFACE = pygame.Surface((self.__width, self.__height))
        pygame.display.set_caption(self.__title)


    def __update_entities(self, entities, player):
        keys = pygame.key.get_pressed()
        rects = []
        for entity in entities:
            rect = pygame.Rect(entity[0], entity[1], 32, 32)
            rects.append(rect)
            pygame.draw.rect(self.__SURFACE, entity[2], rect)
            #entity.update(self.__SURFACE, keys)

        player.update(self.__SURFACE, keys, entities=rects)

    def loop(self, entities, player):
        self.__SURFACE.fill("white")
        self.__update_entities(entities, player)
        self.__win.blit(self.__SURFACE, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__should_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__should_close = True

        self.__clock.tick(60)

        return self.__should_close
