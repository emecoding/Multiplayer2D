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

        self.__deaths = 0
        self.__ignore = ["SPAWN_POINT"]



    def getTime(self):
        return self.__timer__


    def __check_for_win(self, id):
        if id == "WIN":
            self.has_won = True
            self.__timer_is_ticking__ = False

    def __check_for_death(self, id):
        if "KILLER" in str(id):
            return self.__die()

        return False

    def __die(self):
        self.__deaths += 1
        self.respawn()
        return True

    def get_deaths(self):
        return self.__deaths

    def reset_deaths(self):
        self.__deaths = 0

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
            if other[2] == False:
                if other[1] not in self.__ignore:
                    if other[0].colliderect(self.__rect__.x + dx, self.__rect__.y, self.getWidth(), self.getHeight()):
                        self.__check_for_win(other[1])
                        died = self.__check_for_death(other[1])
                        if died == False:
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
            if other[2] == False:
                if other[1] not in self.__ignore:
                    if other[0].colliderect(self.__rect__.x, self.__rect__.y + dy, self.getWidth(), self.getHeight()):
                        self.__check_for_win(other[1])
                        died = self.__check_for_death(other[1])
                        if died == False:
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

        if x < 0:
            self.respawn()
        if x > 800 + self.getWidth():
            self.respawn()
        if y > 600 + self.getHeight():
            self.respawn()

    def __timer_tick(self):
        if self.__timer_is_ticking__:
            self.__timer__ += self.__time_addition__


    def update(self, surf, keys, other_rects, render=True):
        super().update(surf, keys, other_rects, render=render)
        self.__move(keys, other_rects, surf)
        self.__timer_tick()


