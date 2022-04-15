from Config import *
import pygame

class Entity:
    def __init__(self, x, y):
        self.__width, self.__height = 32, 32

        self.__start_x = x
        self.__start_y = y

        self.__rect__ = pygame.Rect(x, y, self.__width, self.__height)
        self.__color__ = (255, 0, 0)
        self.has_won = False

        self.__timer__ = 0
        self.__time_addition__ = 1
        self.__timer_is_ticking__ = True
        self.__current_animation__ = None
        self.__current_frame__ = 0

        self.__facing_right__ = True

    def start_timer(self):
        self.__timer__ = 0
        self.__timer_is_ticking__ = True

    def getX(self):
        return self.__rect__.x

    def getY(self):
        return self.__rect__.y

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getSizeOfDataAsBytes(self, msg):
        s = len(msg)
        return s

    def setPosition(self, x, y):
        self.__rect__.x = x
        self.__rect__.y = y

    def respawn(self):
        self.__rect__.x = self.__start_x
        self.__rect__.y = self.__start_y

    def getDataAsBytes(self):
        msg = f"{self.__rect__.x},{self.__rect__.y},{self.has_won},{float(self.__timer__)}, {self.__current_animation__[self.__current_frame__]['PATH']},{self.__facing_right__}"
        decoded_msg = msg.encode(TEXT_FORMAT)
        size = self.getSizeOfDataAsBytes(msg)
        return decoded_msg, str(size).encode(TEXT_FORMAT), msg

    def getTrueForm(self):
        return [self.__rect__.x, self.__rect__.y]

    def __render(self, surf):
        pygame.draw.rect(surf, self.__color__, self.__rect__)

    def setColor(self, color):
        self.__color__ = color

    def update(self, surf, keys, other_rects, render=True):
        if render:
            self.__render(surf)