import pygame
class OverworldManager:
    def __init__(self, window, player_sprite, background_sprite):
        self.window = window
        self.punkin_sprite = pygame.image.load("img/characters/punkin 1.png").convert_alpha()
        self.player_sprite = pygame.image.load("img/characters/char placeholder 2.png").convert_alpha()
        self.background = pygame.image.load("img/maps/shifty town 1.png").convert()

        self.player_pos = [0.25, 0.36]  # 100 / 800, 100 / 600
        self.punkin_pos = [0.1875, 0.666]  # 150 / 800, 400 / 600
        self.punkin_hitbox = pygame.Rect(
            self.punkin_pos[0],
            self.punkin_pos[1],
            64,
            82
        )
        self.win_w, self.win_h = self.window.get_size()
        self.player_w, self.player_h = int(self.win_w * 0.036), int(self.win_h * 0.1)
        self.player_x = int(self.player_pos[0] * self.win_w) + 5
        self.player_y = int(self.player_pos[1] * self.win_h)
            ####### todo fix player position x so that the footbox aligns with other hitboxes
        self.player_hitbox = pygame.Rect(self.player_x, self.player_y, self.player_w, self.player_h)
        self.player_footbox = pygame.Rect(self.player_x, self.player_y, self.player_w, self.player_h)

        # dialogue timer and response

        self.dialogue_response = None
        self.dialogue_timer = 0
        self.sign_timer = 0
        self.yes_response = 0

        ###### MOVEMENT #####
        self.player_direction = "S"  # default facing south
        self.animations = {}
        for direction in ["N", "S", "E", "W"]:
            frames = []
            for i in range(1, 5):
                path = f"img/characters/walking/proto character {direction}{i}.png"
                frame = pygame.image.load(path).convert_alpha()
                frames.append(frame)
            self.animations[direction] = frames



########### DEBUG MODE ################
        self.debug_mode = False





        ########## house positions #######

        mail_w = 30
        mail_h = 30
        house_h = 100
        house_w = 50

        self.immovable_defs = {
            "house_ul": (0.0785, 0.09, 0.0985, 0.15),  # wider + taller
            "house_dl": (0.0805, 0.652, 0.0985, 0.15),
            "house_ur": (0.825, 0.16, 0.0985, 0.14),
            "house_br": (0.8225, 0.66, 0.0985, 0.14),
            "statue": (0.41375, 0.45, 0.15, 0.069),
            "mail_1": (0.20125, 0.3383, 0.02, 0.05),
            "mail_2": (0.76625, 0.335, 0.02, 0.05),
            "mail_3": (0.64, 0.845, 0.02, 0.05),
            "mail_4": (0.3286, 0.835, 0.02, 0.05),
        }

        #todo make this more modular for other maps
        #todo add interactions
        #todo add text box and portraits


        self.rebuild_immovable_objects()



#### todo refactor display info, make info_box a method that takes text as argument, ** kwargs for enemies, portraits, none for signs
    def display_info(self, punkin_defeated=False):
        info_box = pygame.Rect(30, 450, 700, 150)
        pygame.draw.rect(self.window, (255, 255, 255), info_box, 4)
        pygame.draw.rect(self.window, (0, 0, 0), info_box.inflate(-8, -8))

        portrait_box = pygame.Rect(info_box.x + 20, info_box.y + 20, 100, 100)
        pygame.draw.rect(self.window, (255, 255, 255), portrait_box, 2)
        pygame.draw.rect(self.window, (0, 0, 0), portrait_box.inflate(-4, -4))

        portrait_img = pygame.image.load("img/characters/punkin 1.png").convert_alpha()
        portrait_scaled = pygame.transform.scale(portrait_img, (portrait_box.width - 8, portrait_box.height - 8))
        self.window.blit(portrait_scaled, (portrait_box.x + 4, portrait_box.y + 4))

        font = pygame.font.SysFont(None, 24)

        if self.dialogue_response == "no":
            lines = ["??? : ah man..."]
        elif punkin_defeated or self.dialogue_response == "defeated":
            lines = ["??? : You already beat me..."]
        else:
            lines = ["??? : HI!! WANNA PLAY?"]

        for i, line in enumerate(lines):
            text = font.render(line, True, (255, 255, 255))
            self.window.blit(text, (portrait_box.right + 20, info_box.y + 20 + i * 30))

        # Only show buttons if no response yet
        if self.dialogue_response is None and not punkin_defeated:
            self.yes_button = pygame.Rect(info_box.x + 140, info_box.y + 100, 100, 40)
            self.no_button = pygame.Rect(info_box.x + 260, info_box.y + 100, 100, 40)

            pygame.draw.rect(self.window, (255, 255, 255), self.yes_button, 2)
            pygame.draw.rect(self.window, (255, 255, 255), self.no_button, 2)

            yes_text = font.render("Yes", True, (255, 255, 255))
            no_text = font.render("No", True, (255, 255, 255))
            self.window.blit(yes_text, (self.yes_button.x + 30, self.yes_button.y + 8))
            self.window.blit(no_text, (self.no_button.x + 30, self.no_button.y + 8))

        return True
    def check_statue_collision(self):
        for name, rect in self.immovable_objects.items():
            if name == "statue":

                if self.player_hitbox.colliderect(rect):
                    # self.sign_timer = 60
                    return True

    def signs(self):
        statue_info = ['"Jack: Hero of The Patch"']

        font = pygame.font.SysFont(None, 24)

        info_box = pygame.Rect(30, 450, 700, 150)
        pygame.draw.rect(self.window, (255, 255, 255), info_box, 4)
        pygame.draw.rect(self.window, (0, 0, 0), info_box.inflate(-8, -8))

        text = font.render(statue_info[0], True, (255, 255, 255))
        self.window.blit(text, (info_box.x + 275, info_box.y + 60))

    def get_direction(self, keys):
        if keys[pygame.K_a]:
            return "W"
        elif keys[pygame.K_d]:
            return "E"
        elif keys[pygame.K_w]:
            return "N"
        elif keys[pygame.K_s]:
            return "S"
        return None

    def update_player_hitbox(self):
        self.player_x = int(self.player_pos[0] * self.win_w)
        self.player_y = int(self.player_pos[1] * self.win_h)
        self.player_h_scale = self.player_h * 1.5

        # Full-body hitbox
        self.player_hitbox.update(self.player_x, self.player_y, self.player_w* 1.5, self.player_h * 1.5)

        # Footbox (bottom 20% of sprite)
        foot_h = int(self.player_h * 1.5 * 0.2)
        foot_y = self.player_y + self.player_h - foot_h
        foot_x = self.player_x + int(self.player_w * 0.1)  # optional horizontal padding
        foot_w = int(self.player_w * 0.8)
        self.player_footbox.update(foot_x, foot_y, foot_w, foot_h)
#### todo fix hitboxes wowza theyre messed up
    def make_scaled_rect(self,x_r, y_r, w_r, h_r):
        x = int(x_r * self.win_w)
        y = int(y_r * self.win_h)
        w = int(w_r * self.win_w)
        h = int(h_r * self.win_h)
        return pygame.Rect(x, y, w, h)

    def check_collision(self):


### todo make this work for any enemy (actually update to reflect enemies that talk and those that dont)

        punkin_w, punkin_h = int(self.win_w * 0.08), int(self.win_h * 0.14)
        punkin_x = int(self.punkin_pos[0] * self.win_w)
        punkin_y = int(self.punkin_pos[1] * self.win_h)
        punkin_hitbox = pygame.Rect(punkin_x, punkin_y, punkin_w, punkin_h)

        return self.player_hitbox.colliderect(punkin_hitbox)

    def check_collide_obj(self):
        for name, rect in self.immovable_objects.items():
            if self.player_footbox.colliderect(rect):
                print(f"Collided with {name}")
                return True
        return False
### todo make modular for any immovable
    def rebuild_immovable_objects(self):
        self.immovable_objects = {}
        for name, (x_r, y_r, w_r, h_r) in self.immovable_defs.items():
            self.immovable_objects[name] = self.make_scaled_rect(x_r, y_r, w_r, h_r)

    def set_animation(self, direction):
        if direction in self.animations:

            self.walking_frames = self.animations[direction]
            print(f"SET ANIMATION: {direction}, frames loaded:", len(self.walking_frames))
            self.walking_frame_index = 0
            self.walking_timer = 0
        else:
            print(f"Unknown direction: {direction}")


    def animate_player(self, direction):
        self.walking_frames = []

        for i in range(1,5):
            frame = pygame.image.load(
                f"img/characters/walking/proto character {direction}{i}.png").convert_alpha()
            self.walking_frames.append(frame)
        self.walking_frame_index = 0
        self.walking_timer = 0
    def draw(self):
        win_w, win_h = self.window.get_size()
        self.rebuild_immovable_objects()

        # Scale and draw background
        bg_scaled = pygame.transform.scale(self.background, (win_w, win_h))
        self.window.blit(bg_scaled, (0, 0))

        # Scale and draw punkin
        punkin_w, punkin_h = int(win_w * 0.08), int(win_h * 0.14)
        punkin_x = int(self.punkin_pos[0] * win_w)
        punkin_y = int(self.punkin_pos[1] * win_h)
        punkin_scaled = pygame.transform.scale(self.punkin_sprite, (punkin_w, punkin_h))
        self.punkin_hitbox = pygame.Rect(self.punkin_pos[0], self.punkin_pos[1], 64, 82)
        self.window.blit(punkin_scaled, (punkin_x, punkin_y))

        # Scale and draw player

        player_w, player_h = (self.player_w * 1.5), (self.player_h * 1.5)
        player_x = int(self.player_pos[0] * win_w)
        player_y = int(self.player_pos[1] * win_h)

        # Use animated frame if moving, else fallback to idle sprite
        if self.is_moving and hasattr(self, "walking_frames"):
            frame = self.walking_frames[self.walking_frame_index]
        else:
            frame = self.player_sprite  # fallback idle sprite

        player_scaled = pygame.transform.scale(frame, (player_w, player_h))
        self.window.blit(player_scaled, (player_x, player_y))
        self.update_player_hitbox()
        self.update_walk_animation()


        #### draw statue on top #########
        statue_top = pygame.image.load("img/maps/statue_top.png").convert_alpha()
        stat_scaled = pygame.transform.scale(statue_top, (win_w, win_h))
        self.window.blit(stat_scaled, (0, 0))

        ######### Test Walls ########
        if self.debug_mode:

            pygame.draw.rect(self.window, (255, 0, 0), self.player_hitbox, 2)
            pygame.draw.rect(self.window, (0, 255, 0), self.player_footbox, 2)
            pygame.draw.rect(self.window, (0, 0, 255), self.punkin_hitbox, 2)
            for name, rect in self.immovable_objects.items():
                pygame.draw.rect(self.window, (255, 0, 0), rect, 2)
                font = pygame.font.SysFont(None, 20)
                label = font.render(name, True, (255, 255, 255))
                self.window.blit(label, (rect.x, rect.y - 18))
            pygame.draw.rect(self.window, (255, 0, 0), self.player_footbox, 2)

    def update_walk_animation(self):
        if self.is_moving and hasattr(self, "walking_frames"):
            self.walking_timer += 1
            if self.walking_timer >= 12:
                print("Frame:", self.walking_frame_index, "/", len(self.walking_frames))
                self.walking_frame_index = (self.walking_frame_index + 1) % len(self.walking_frames)
                self.walking_timer = 0

    def move_player(self, direction):
        print("moving")
        move_speed = 0.005
        next_pos = self.player_pos.copy()

        if direction != self.player_direction:
            self.set_animation(direction)
            self.player_direction = direction
        self.is_moving = True

        if direction == "W":

            next_pos[0] -= move_speed
        elif direction == "E":

            next_pos[0] += move_speed
        elif direction == "N":
            next_pos[1] -= move_speed
        elif direction == "S":
            next_pos[1] += move_speed

        next_pos[0] = max(0, min(1, next_pos[0]))
        next_pos[1] = max(0, min(1, next_pos[1]))

        next_x = int(next_pos[0] * self.win_w)
        next_y = int(next_pos[1] * self.win_h)
        foot_h = int(self.player_h * 0.2)
        foot_y = next_y + self.player_h - foot_h
        next_footbox = pygame.Rect(next_x, foot_y, self.player_w, foot_h)

        for rect in self.immovable_objects.values():
            if next_footbox.colliderect(rect):
                return

        self.player_pos = next_pos
        self.update_player_hitbox()
        for rect in self.immovable_objects.values():
            if next_footbox.colliderect(rect):
                return  # Block movement

        self.player_pos = next_pos
        self.update_player_hitbox()



    def process_input(self, keys):

        direction = self.get_direction(keys)
        self.is_moving = False

        if direction:

            self.move_player(direction)


        # Interaction logic
        if keys[pygame.K_SPACE] and self.player_hitbox.colliderect(self.punkin_hitbox):
            self.display_info()

    def move_npc(self, npc):
        pass

    ### todo get good and add animations, overlays, research draw order