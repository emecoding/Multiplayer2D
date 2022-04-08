from Config import *
import pygame

class Entity:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__width, self.__height = 32, 32

        self.__rect__ = pygame.Rect(self.__x, self.__y, self.__width, self.__height)
        self.__color__ = (255, 0, 0)

    def getX(self):
        return self.__rect__.x

    def getY(self):
        return self.__rect__.y

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getSizeOfPositionAsBytes(self, msg):
        s = len(msg)
        return s

    def setPosition(self, x, y):
        self.__rect__.x = x
        self.__rect__.y = y

    def getPositionAsBytes(self):
        msg = f"{self.__rect__.x},{self.__rect__.y}".encode(TEXT_FORMAT)
        size = self.getSizeOfPositionAsBytes(msg)
        return msg, str(size).encode(TEXT_FORMAT)

    def getTrueForm(self):
        return [self.__x, self.__y, self.__color__]

    def __render(self, surf):
        pygame.draw.rect(surf, self.__color__, self.__rect__)

    def setColor(self, color):
        self.__color__ = color

    def update(self, surf, keys, render=True, entities=None):
        if render:
            self.__render(surf)