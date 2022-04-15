import random, os

from Entity import Entity
from Config import *
import pygame
pygame.init()

PLAYERS = ["Clone", "Shroom"]

class Player(Entity):
    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.__color__ = (0, 0, 255)
        self.__name = name
        self.__speed = 5
        self.__vel_y = 0
        self.__acc_y = 0.3
        self.__jump_force = 20
        self.__is_grounded = False
        self.__jumped = False
        self.__shoot_range = 100


        self.__deaths = 0
        self.__ignore = ["SPAWN_POINT"]

        self.__font = pygame.font.SysFont('freesansbold.ttf', 32)
        self.__name_text = self.__font.render(self.__name, True, (0, 0, 0), (255, 255, 255))
        self.__name_text_rect = self.__name_text.get_rect(center=self.__rect__.center)

        self.__idle_frames_right, self.__idle_frames_left, self.__run_frames_right, self.__run_frames_left = self.get_random_player_animations()
        self.__current_animation__ = self.__idle_frames_right

        self.__frame_rate = 20
        self.__frame_tick = 0

    def get_random_player_animations(self):
        name = random.choice(PLAYERS)
        abs_path = os.path.abspath(f"Images/Players/{name}")
        abs_path_idle = os.path.abspath(f"{abs_path}/Idle")
        abs_path_run = os.path.abspath(f"{abs_path}/Run")

        items_in_idle = os.listdir(abs_path_idle)
        items_in_run = os.listdir(abs_path_run)

        idle_frames_right = self.__convert_items_to_images(items_in_idle, f"Images/Players/{name}/Idle")
        idle_frames_left = self.__convert_items_to_images(items_in_idle, f"Images/Players/{name}/Idle", rotate=True)
        run_frames_right = self.__convert_items_to_images(items_in_run, f"Images/Players/{name}/Run")
        run_frames_left = self.__convert_items_to_images(items_in_run, f"Images/Players/{name}/Run", rotate=True)

        return idle_frames_right, idle_frames_left, run_frames_right, run_frames_left

    def __convert_items_to_images(self, items, abs_path, rotate=False):
        images = []
        for item in items:
            path = abs_path + f"/{item}"
            image = {"IMG":pygame.image.load(path), "PATH":path}
            if rotate:
                image["IMG"] = pygame.transform.flip(image["IMG"], True, False)
            images.append(image)

        return images

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
            self.__facing_right__ = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.__speed
            self.__facing_right__ = False

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

        if dx != 0:
            if self.__facing_right__:
                self.__current_animation__ = self.__run_frames_right
            else:
                self.__current_animation__ = self.__run_frames_left
        else:
            if self.__facing_right__:
                self.__current_animation__ = self.__idle_frames_right
            else:
                self.__current_animation__ = self.__idle_frames_left


        if x < 0:
            self.respawn()
        if x > 800 + self.getWidth():
            self.respawn()
        if y > 600 + self.getHeight():
            self.respawn()

    def __timer_tick(self):
        if self.__timer_is_ticking__:
            self.__timer__ += self.__time_addition__

    def __animate(self, surf):
        self.__frame_tick += 1
        if self.__frame_tick >= self.__frame_rate:
            self.__frame_tick = 0
            self.__current_frame__ += 1

        if self.__current_frame__ >= len(self.__current_animation__):
            self.__current_frame__ = 0

        surf.blit(self.__current_animation__[self.__current_frame__]["IMG"], self.__rect__)


    def update(self, surf, keys, other_rects, render=False):
        super().update(surf, keys, other_rects, render=render)
        self.__move(keys, other_rects, surf)
        self.__timer_tick()

        self.__name_text_rect = self.__name_text.get_rect(center=self.__rect__.center)
        surf.blit(self.__name_text, (self.__name_text_rect[0], self.__name_text_rect[1] - 30))

        self.__animate(surf)

