import pygame, json, sys, os

pygame.font.init()

class Button:
    def __init__(self, img, x, y, id):
        self.__img = img
        self.__x = x
        self.__y = y
        self.__id = id
    
    def render(self, win):
        win.blit(self.__img, (self.__x, self.__y))


    def get_rect(self): return pygame.Rect(self.__x, self.__y, 32, 32)

    def get_entity(self, x, y): return LevelEntity(self.__img, x, y, self.__id, False)

    def get_img(self): return self.__img
    def get_id(self): return self.__id


class LevelEntity:
    def __init__(self, img, x, y, id, col):
        self.__img = img
        self.__x = x
        self.__y = y

        self.__start_x = x
        self.__start_y = y

        self.__dif_x = 0
        self.__dif_y = 0

        self.__id = id
        self.__col = col
        self.__items = []
        self.__width = 32
        self.__height = 32

        self.__is_background = False

    def add_item(self, item): self.__items.append(item)

    def get_collision_detection(self): return self.__col

    def get_img(self):
        try:
            self.__img = pygame.transform.scale(self.__img, (self.__width, self.__height))
        except:
            print("Fucker")
        return self.__img
    def get_id(self): return self.__id
    def get_items(self):
        lst = []
        for item in self.__items:
            lst.append(item["id"])

        return lst



    def get_rect(self): return pygame.Rect(self.__x, self.__y, self.__width, self.__height)
    def get_position(self): return [self.__start_x, self.__start_y]
    def get_current_position(self): return [self.__x, self.__y]
    def set_position(self, x, y):
        self.__x = x
        self.__y = y
    def set_collision_detection(self, c): self.__col = c
    def set_dif(self, x, y):
        self.__dif_x = x
        self.__dif_y = y
    def get_dif(self): return [self.__dif_x, self.__dif_y]

    def is_background(self):
        return self.__is_background

    def set_as_background(self, b, win_size):
        self.__is_background = b
        if self.__is_background:
            self.set_collision_detection(False)
            self.__width = win_size[0]/2
            self.__height = win_size[1]/2
            self.set_position(0, 0)
        else:
            self.__width = 32
            self.__height = 32

class LevelEditor:
    def __init__(self, file_type):
        self.__entities = []

        self.__TILE_WIDTH = 32
        self.__TILE_HEIGHT = 32

        self.__MOVEMENT_SPEED = 1

        self.__GRID_COLOR = (0, 0, 0)
        self.__WIN_WIDTH = 800
        self.__WIN_HEIGHT = 640

        self.__level_name = self.__get_level_name()

        self.__block_data = self.__get_block_data()

        self.__file_type = file_type
        if self.__if_load_old_file():
            self.__entities = self.__load_old_file()
            self.__level_file = self.__get_file_path()
        else:
            self.__level_file = self.__create_level_file_based_on_level_name()

        self.__screen = pygame.display.set_mode((self.__WIN_WIDTH, self.__WIN_HEIGHT))
        pygame.display.set_caption("Level editor")

        self.__buttons = self.__create_buttons()

        self.__collision_detection = True

        self.__font = pygame.font.Font('freesansbold.ttf', 16)

        self.__active_entity = None



        self.__help_win_is_open = False
        self.__help_win_stuff = []

        self.__main_loop()

    def __get_file_path(self):
        return "Files/" + self.__level_name + self.__file_type

    def __get_proper_image_path(self, path):
        l = os.getcwd().replace("Levels", path)
        s = ""
        for a in l:
            if a == "/":
                s += os.sep
            else:
                s += a
        return s

    def __load_old_file(self):
        entities = []
        data = {}

        with open(self.__get_file_path(), "r") as file:
            data = json.loads(file.read())
            file.close()

        self.__WIN_WIDTH = data["PROJECT"]["WIN_WIDTH"]
        self.__WIN_HEIGHT = data["PROJECT"]["WIN_HEIGHT"]
        self.__TILE_WIDTH = data["PROJECT"]["TILE_WIDTH"]
        self.__TILE_HEIGHT = data["PROJECT"]["TILE_HEIGHT"]
        self.__MOVEMENT_SPEED = data["PROJECT"]["EDITOR_MOVEMENT_SPEED"]
        self.__GRID_COLOR = data["PROJECT"]["GRID_COLOR"]

        for e in data["ENTITIES"]:
            for i in range(len(self.__block_data["BLOCKS"])):
                if e["id"] == self.__block_data["BLOCKS"][i]["id"]:
                    path = self.__get_proper_image_path(self.__block_data["BLOCKS"][i]["image"]).replace("Leveleditor", f"{self.__block_data['BLOCKS'][i]['image']}")
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img, (self.__TILE_WIDTH, self.__TILE_HEIGHT))
                    entity = LevelEntity(img, e["x"], e["y"], e["id"], e["collision"])

                    for i in range(len(e["items"])): 
                        entity.add_item({"id": self.__block_data["BLOCKS"][i]["id"]})
                    
                    entities.append(entity)


        return entities

    def __if_load_old_file(self):
        return os.path.isfile(self.__get_file_path())

    def __create_level_file_based_on_level_name(self):
        d = self.__get_file_path()
        try:
            with open(d, "w") as file: file.close()
        except:
            print("Error with level file creation!")


        return d


    def __create_buttons(self):
        btns = []
        x = 0
        y = 500
        for i in range(len(self.__block_data["BLOCKS"])):
            dir = self.__block_data["BLOCKS"][i]["image"]
            newDir = os.getcwd().replace("Levels", dir)

            s = ""
            for a in newDir:
                if a == "/":
                    s += os.sep
                else:
                    s += a

            s = s.replace("Leveleditor", dir)
            img = pygame.image.load(s)
            img = pygame.transform.scale(img, (self.__TILE_WIDTH, self.__TILE_HEIGHT))
            btn = Button(img, x, y, self.__block_data["BLOCKS"][i]["id"])
            btns.append(btn)
            x += 35

            if x >= 770:
                x = 0
                y += 35

        return btns

    def __get_block_data(self):
        data = {}
        with open("BlockData.json", "r") as file:
            data = json.loads(file.read())
            file.close()
        return data

    def __get_level_name(self):
        return input("What is the level name: ")

    def __save(self):
        for e in self.__entities:
            e.set_position(e.get_position()[0], e.get_position()[1])


        data = {
            "PROJECT": {
                "WIN_WIDTH": self.__WIN_WIDTH,
                "WIN_HEIGHT": self.__WIN_HEIGHT,
                "TILE_WIDTH": self.__TILE_WIDTH,
                "TILE_HEIGHT": self.__TILE_HEIGHT,
                "EDITOR_MOVEMENT_SPEED": self.__MOVEMENT_SPEED,
                "GRID_COLOR": self.__GRID_COLOR
            },

            "ENTITIES": [

            ]
        }

        for e in self.__entities:
            new_data = {"id": e.get_id(),
                        "x": e.get_position()[0] + e.get_dif()[0],
                        "y": e.get_position()[1] + e.get_dif()[1],
                        "collision": e.get_collision_detection(),
                        "items": e.get_items()
                        }
            data["ENTITIES"].append(new_data)

        print(f"Saving at: '{self.__level_file}'...")

        with open(self.__level_file, "w+") as file:
            file.write(json.dumps(data, indent=4))
            file.close()

        print("Done saving!")

    def exit(self):
        self.__save()
        pygame.quit()
        sys.exit()

    def __render_buttons_for_blocks(self):
        for btn in self.__buttons:
            btn.render(self.__screen)

            
    def __check_buttons_for_clicks(self):
        r = self.__get_editor_mouse()
        left_click = pygame.mouse.get_pressed(num_buttons=3)[0]
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(self.__screen, (255, 0, 0), r)
        for btn in self.__buttons:
            if r.colliderect(btn.get_rect()):
                if left_click:
                    self.__active_entity = btn.get_entity(mouse_pos[0], mouse_pos[1])
                    break
            
    def __check_for_build(self):
        left_click = pygame.mouse.get_pressed(num_buttons=3)[2]

        mouse_pos = pygame.mouse.get_pos()
        if self.__active_entity != None:
            self.__active_entity.set_position(int(mouse_pos[0]/self.__TILE_WIDTH)*self.__TILE_WIDTH, int(mouse_pos[1]/self.__TILE_HEIGHT)*self.__TILE_HEIGHT)

        if left_click and self.__active_entity != None:
            r = self.__get_editor_mouse()
            can_build = True
            for i in self.__entities:
                if r.colliderect(i.get_rect()):
                    can_build = False
                    break
                else:
                    can_build = True

            if can_build:
                i = LevelEntity(self.__active_entity.get_img(), self.__active_entity.get_current_position()[0], self.__active_entity.get_current_position()[1], self.__active_entity.get_id(), self.__collision_detection)
                self.__entities.append(i)



    def __render_entities(self):
        for e in self.__entities:
            if (e.get_position()[0] + e.get_dif()[0] != e.get_current_position()[0]):
                e.set_position(e.get_current_position()[0] + e.get_dif()[0], e.get_current_position()[1])
            if (e.get_position()[1] + e.get_dif()[1] != e.get_current_position()[1]):
                e.set_position(e.get_current_position()[0], e.get_current_position()[1] + e.get_dif()[1])


            self.__screen.blit(e.get_img(), e.get_current_position())
            if e.get_collision_detection():
                pygame.draw.rect(self.__screen, (255, 0, 0), e.get_rect(), 1)


    def __toggle_entitys_collision_detection(self):
        r = self.__get_editor_mouse()
            
        for e in self.__entities:
            if r.colliderect(e.get_rect()):
                if e.get_collision_detection(): e.set_collision_detection(False)
                else: e.set_collision_detection(True)
                break

    def __check_for_input(self):
        keys = pygame.key.get_pressed()
        r = self.__get_editor_mouse()
        if keys[pygame.K_e]:
            for e in self.__entities:
                if r.colliderect(e.get_rect()):
                    self.__entities.remove(e)
                    break


    def __render_grid(self):
        for y in range(int(self.__WIN_HEIGHT/self.__TILE_HEIGHT)):
            for x in range(int(self.__WIN_WIDTH/self.__TILE_WIDTH)):
                pygame.draw.rect(self.__screen, self.__GRID_COLOR, pygame.Rect(x*self.__TILE_WIDTH, y*self.__TILE_HEIGHT, self.__TILE_WIDTH, self.__TILE_HEIGHT), 1)

    def __clear(self):
        for e in self.__entities:
            e.set_position(e.get_position()[0], e.get_position()[1])
        
        self.__entities.clear()

    def __get_editor_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        return pygame.Rect(mouse_pos[0] - 5, mouse_pos[1], 10, 10)

    def __check_if_set_items(self):
        r = self.__get_editor_mouse()
        for e in self.__entities:
            if r.colliderect(e.get_rect()):
                for i in range(len(self.__block_data["BLOCKS"])):
                    if e.get_id() == self.__block_data["BLOCKS"][i]["id"]:
                        print("-----------------")
                        print(f"SET ITEMS FOR {self.__block_data['BLOCKS'][i]['id']}")
                        how_many = input("How many items do you want to assign: ")
                        for j in range(int(how_many)):
                            item_id = input("ID for item: ")
                            item = None
                            for it in range(len(self.__block_data["BLOCKS"])):
                                if self.__block_data["BLOCKS"][it]["id"] == item_id:
                                    item = {"id": self.__block_data["BLOCKS"][it]["id"]}
                                    e.add_item(item)
                                    print("ITEM ADDED!")
                                    break

                            if item == None:
                                print("ITEM NOT FOUND!")
                break

    def __open_help_win(self):
        self.__help_win_stuff.clear()
        tile_width_text = self.__font.render(f"Tile width: '{str(self.__TILE_WIDTH)}'", False, (0, 0, 0), (255, 255, 255))
        tile_height_text = self.__font.render(f"Tile height: '{str(self.__TILE_HEIGHT)}'", False, (0, 0, 0), (255, 255, 255))
        build_text = self.__font.render(f"Build with 'left click'", False, (0, 0, 0), (255, 255, 255))
        rubber_text = self.__font.render(f"Use rubber with: 'e'", False, (0, 0, 0), (255, 255, 255))
        toggle_collisions = self.__font.render(f"Toggle collision from one entity with 'f'", False, (0, 0, 0), (255, 255, 255))
        toggle_collisions2 = self.__font.render(f"Toggle collision from many entities with 'c'", False, (0, 0, 0),
                                                (255, 255, 255))
        save_text = self.__font.render(f"Save with 's'", False, (0, 0, 0), (255, 255, 255))
        clear_text = self.__font.render(f"Clear with 'q'", False, (0, 0, 0), (255, 255, 255))
        move_entities = self.__font.render(f"Move in scene with arrow keys", False, (0, 0, 0), (255, 255, 255))
        set_items_text = self.__font.render(f"Set items for entity with 'i'", False, (0, 0, 0), (255, 255, 255))
        movement_speed = self.__font.render(f"Current editor movement speed is '{str(self.__MOVEMENT_SPEED)}'. Set new movement speed with 'l'", False, (0, 0, 0), (255, 255, 255))
        grid_color_text = self.__font.render(f"Current grid color is: '{str(self.__GRID_COLOR)}'. Set new grid color with 'u'", False, (0, 0, 0), (255, 255, 255))
        win_width = self.__font.render(f"Current window width is: '{str(self.__WIN_WIDTH)}'", False, (0, 0, 0), (255, 255, 255))
        win_height = self.__font.render(f"Current window height is: '{str(self.__WIN_HEIGHT)}'", False, (0, 0, 0),
                                       (255, 255, 255))



        self.__help_win_stuff.append(tile_width_text)
        self.__help_win_stuff.append(tile_height_text)
        self.__help_win_stuff.append(build_text)
        self.__help_win_stuff.append(rubber_text)
        self.__help_win_stuff.append(toggle_collisions)
        self.__help_win_stuff.append(toggle_collisions2)
        self.__help_win_stuff.append(save_text)
        self.__help_win_stuff.append(clear_text)
        self.__help_win_stuff.append(move_entities)
        self.__help_win_stuff.append(set_items_text)
        self.__help_win_stuff.append(movement_speed)
        self.__help_win_stuff.append(grid_color_text)
        self.__help_win_stuff.append(win_width)
        self.__help_win_stuff.append(win_height)

    def __set_new_grid_color(self):
        r = int(input("Red: "))
        if r < 0: r = 0
        if r > 255: r = 255
        g = int(input("Green: "))
        if g < 0: g = 0
        if g > 255: g = 255
        b = int(input("Blue: "))
        if b < 0: b = 0
        if b > 255: b = 255

        self.__GRID_COLOR = (r, g, b)


    def __set_new_movement_speed(self):
        new_movement_speed = int(input("Set new movement speed: "))
        self.__MOVEMENT_SPEED = new_movement_speed

    def __check_for_setting_background(self):
        r = self.__get_editor_mouse()
        for entity in self.__entities:
            if entity.get_rect().colliderect(r):
                if entity.is_background(): entity.set_as_background(False, (self.__WIN_WIDTH, self.__WIN_HEIGHT))
                elif entity.is_background() == False: entity.set_as_background(True, (self.__WIN_WIDTH, self.__WIN_HEIGHT))
                else: print("You fucked up....")
                print(entity.is_background())
                break

    def __main_loop(self):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.__screen.fill((255, 255, 255))
            self.__render_grid()
            self.__check_for_build()
            self.__render_entities()
            self.__render_buttons_for_blocks()
            self.__check_buttons_for_clicks()
            self.__check_for_input()

            if self.__active_entity != None:
                self.__screen.blit(self.__active_entity.get_img(), (int(mouse_pos[0]/self.__TILE_WIDTH)*self.__TILE_WIDTH, int(mouse_pos[1]/self.__TILE_HEIGHT)*self.__TILE_HEIGHT))
            


            tile_win_y = 0
            if self.__help_win_is_open:
                for stuff in self.__help_win_stuff:
                    self.__screen.blit(stuff, (0, tile_win_y))
                    tile_win_y += 16
            else:
                text = self.__font.render(f'Collision detection: {str(self.__collision_detection)}', False, (0, 0, 0),
                                          (255, 255, 255))
                self.__screen.blit(text, (0, 50))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        if self.__collision_detection: self.__collision_detection = False
                        else: self.__collision_detection = True
                    if event.key == pygame.K_f:
                        self.__toggle_entitys_collision_detection()
                    if event.key == pygame.K_s:
                        self.__save()
                    if event.key == pygame.K_q:
                        self.__clear()
                    if event.key == pygame.K_l:
                        self.__set_new_movement_speed()
                    if event.key == pygame.K_u:
                        self.__set_new_grid_color()
                    #if event.key == pygame.K_b:
                     #   self.__check_for_setting_background()

                    if event.key == pygame.K_LEFT:
                        for e in self.__entities:
                            e.set_dif(e.get_dif()[0] + self.__TILE_WIDTH*self.__MOVEMENT_SPEED, e.get_dif()[1])
                            e.set_position(e.get_current_position()[0] + self.__TILE_WIDTH*self.__MOVEMENT_SPEED, e.get_current_position()[1])
                    if event.key == pygame.K_RIGHT:
                        for e in self.__entities:
                            e.set_dif(e.get_dif()[0] - self.__TILE_WIDTH*self.__MOVEMENT_SPEED, e.get_dif()[1])
                            e.set_position(e.get_current_position()[0] - self.__TILE_WIDTH*self.__MOVEMENT_SPEED, e.get_current_position()[1])

                    if event.key == pygame.K_UP:
                        for e in self.__entities:
                            e.set_dif(e.get_dif()[0], e.get_dif()[1] + self.__TILE_HEIGHT*self.__MOVEMENT_SPEED)
                            e.set_position(e.get_current_position()[0], e.get_current_position()[1] + self.__TILE_HEIGHT*self.__MOVEMENT_SPEED)
                    if event.key == pygame.K_DOWN:
                        for e in self.__entities:
                            e.set_dif(e.get_dif()[0], e.get_dif()[1] - self.__TILE_HEIGHT*self.__MOVEMENT_SPEED)
                            e.set_position(e.get_current_position()[0], e.get_current_position()[1] - self.__TILE_HEIGHT*self.__MOVEMENT_SPEED)


                    if event.key == pygame.K_i:
                        self.__check_if_set_items()
                    if event.key == pygame.K_ESCAPE:
                        if self.__help_win_is_open:
                            self.__help_win_is_open = False
                        else:
                            self.__help_win_is_open = True
                            self.__open_help_win()

            clock.tick(60)



editor = LevelEditor(".json")