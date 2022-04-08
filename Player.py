from Entity import Entity
from Config import *
import pygame
pygame.init()

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__color__ = (0, 0, 255)
        self.__speed = 5
        self.__vel_y = 0
        self.__acc_y = 0.3
        self.__jump_force = 20
        self.__is_grounded = False
        self.__jumped = False
        self.__shoot_range = 100
        self.__facing_right = True

    def __hor_movement_collision(self, lst, DX):
        dx = DX
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.__speed
            self.__facing_right = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.__speed
            self.__facing_right = False

        for other in lst:
            if other[0].colliderect(self.__rect__.x + dx, self.__rect__.y, self.getWidth(), self.getHeight()):
                if dx > 0:
                    self.__rect__.right = other[0].left
                elif dx < 0:
                    self.__rect__.left = other[0].right
                dx = 0

        self.__rect__.x += dx

        return dx

    def __ver_movement_collision(self, lst, DY):
        dy = DY
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.__jumped == False:
            self.__vel_y = -self.__jump_force
            self.__jumped = True

        self.__vel_y += 1
        if self.__vel_y > 10:
            self.__vel_y = 10

        dy += self.__vel_y

        for other in lst:
            if other[0].colliderect(self.__rect__.x, self.__rect__.y + dy, self.getWidth(), self.getHeight()):
                if self.__vel_y < 0:
                    dy = 0
                    self.__vel_y = 0
                elif self.__vel_y >= 0:
                    dy = 0
                    self.__jumped = False
                    self.__vel_y = 0

        if self.__rect__.y + dy >= 600 - self.getHeight():
            dy = 0
            self.__jumped = False
            self.__vel_y = 0

        self.__rect__.y += dy

        return dy


    def __move(self, keys, entities, surf):
        x = self.getX()
        y = self.getY()
        dx = 0
        dy = 0

        dx = self.__hor_movement_collision(entities, dx)
        dy = self.__ver_movement_collision(entities, dy)

        if keys[pygame.K_SPACE] or keys[pygame.K_DOWN]:
            rect = None
            if self.__facing_right:
                rect = pygame.Rect(x + self.getWidth(), y, self.__shoot_range, 20)
            else:
                rect = pygame.Rect(x - self.__shoot_range, y, self.__shoot_range, 20)

            pygame.draw.rect(surf, (255, 0, 0), rect)
            for other in entities:
                if other[0].colliderect(rect):
                    other[1] -= 1
                    other[2] = ENTITY_STATUS_TAKE_DAMAGE
                else:
                    other[2] = ENTITY_STATUS_NEUTRAL

        '''if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.__speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.__speed

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.__is_grounded:
            dy -= self.__jump_force



        if y < 600 - self.getHeight():
            self.__vel_y += self.__acc_y
            self.__is_grounded = False
        else:
            self.__vel_y = 0
            y = 600 - self.getHeight()
            self.__is_grounded = True

        dy += self.__vel_y

        x += dx
        y += dy

        self.setPosition(x, y)'''



    def update(self, surf, keys, render=True, entities=None):
        super().update(surf, keys, render=render)
        self.__move(keys, entities, surf)


