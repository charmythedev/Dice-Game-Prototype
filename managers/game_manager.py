from managers.character_class import Character
from managers.deck import *
from managers.scene_manager import SceneManager
import pygame

from managers.ui_manager import UIManager
import random
from managers.overworld_manager import OverworldManager
class GameManager:

    def __init__(self, window):
        self.sm = SceneManager()

        #### timers ####
        self.win_timer = 0

        ## state and ui ##
        self.state = "menu"
        self.window = window
        self.dialogue_active = False
        self.dialogue_result = None
        self.dialogue_triggered = False
        self.combat_backgrounds = {
            "punkin": "img/bg/punkin_bg.png",
        }

        ### KEYS ####

        self.keys = pygame.key.get_pressed()

        #sprites and drawing#
        self.player = Character("Player", "warrior", 100, 100,0, ProtoDeck)
        self.enemy = Character("lesser punkin", "trickster", 5, 50,0, EnemyDeck)
        self.enemy.sprite_path = "img/characters/punkin 1.png"
        self.player.sprite_path = "img/character png.png"
        self.background_sprite = pygame.image.load("img/maps/shifty town 1.png").convert()
        self.combat_background = pygame.image.load(self.combat_backgrounds["punkin"]).convert()

        ##music##
        pygame.mixer.init()
        self.select_sound = pygame.mixer.Sound("music/select.mp3")
        self.current_music = None

        #### enemy tokens ####
        self.punkin_token = "1"
        self.player_tokens = []
        self.punkin_defeated = False

        ## managers ##
        self.ui = UIManager(window)
        self.overworld = OverworldManager(self.window, self.player, self.background_sprite)

        self.player_current_health = self.player.health

        # Initial setup for combat
        self.enemy_turn_pending = False
        self.enemy_action_text = ""
        self.enemy_text_timer = 0

        self.turn_phase = self.first_turn()
        self.game_over = False
        self.first_turn_flag = True
        self.enemy_first_turn = True
        if self.turn_phase == "player":
            self.prepare_player_turn()
        else:
            self.enemy_turn_pending = True  # queue enemy turn if enemy starts

    #### debug ###

    def music(self):
        state_to_music = {
             "menu": r"C:\Users\trevo\PycharmProjects\dice_game_proto_v1\music\sad theme.mp3",
             "game over": "music/tranquil.mp3",
             "playing": "music/fight combat v1.mp3",
             "overworld": "music/tranquil.mp3",
             "credits": "music/credits.mp3",

         }

        desired_music = state_to_music.get(self.state)

        if desired_music and self.current_music != desired_music:
             pygame.mixer.music.load(desired_music)
             pygame.mixer.music.play(-1)
             self.current_music = desired_music

        #todo change init to allow different "player" or "enemy" to be passed in
        #todo fix enemy ai to play more than one card if available
        #todo fix gameplay flow to allow for big hits and more fun less time in combat


    def first_turn(self):
        player_dice_roll = random.randint(1, 6)
        enemy_dice_roll = random.randint(1, 6)
        return "player" if player_dice_roll > enemy_dice_roll else "enemy"

    def prepare_player_turn(self):
        print("Preparing player turn")
        self.player.roll_dice()
        draw_amount = 5 if self.first_turn_flag else 1 + self.player.draw_bonus
        self.player.draw_cards(draw_amount)
        self.player.draw_bonus = 0
        self.player.defense = 0
        self.first_turn_flag = False
        self.player.rerolls = self.player.base_rerolls + self.player.bonus_rerolls

        self.ui.current_button = "next"
        print("set button to NEXT")

        self.ui.selected_dice.clear()
        self.ui.combo_amt = ""




    def enemy_turn(self):
        print("Enemy turn begins")
        self.enemy.roll_dice()
        self.enemy.defense =0
        draw_amount = 5 if self.enemy_first_turn else 1 + self.enemy.draw_bonus
        self.enemy.draw_cards(draw_amount)
        self.enemy.draw_bonus = 0
        self.enemy_first_turn = False
        self.win_timer = 0

        combo_score, _ = self.enemy.check_combo(self.enemy.rolls)
        self.enemy.calc_energy(self.enemy.rolls, combo_score)

        for card in self.enemy.hand[:]:
            if self.enemy.energy >= card.cost and card.card_type == "attack":
                self.enemy.activate_card(card, self.player)
                self.enemy.deck.discard_pile.append(card)

                self.enemy_action_text = f"{self.enemy.name} played {card.name}"

                # self.ui.dam_shake(self.player,self.player_x,self.player_y)
                print(f"{self.enemy.name} played {card.name}")
                self.enemy_text_timer = 120  # ~2 seconds at 60 FPS

                break

        self.turn_phase = "player"
        self.prepare_player_turn()

    def handle_click(self, event):
        if self.state == "menu":

            if event.type == pygame.KEYDOWN:
                self.select_sound.play()
                # self.start_combat()
                self.state = "overworld"


            elif event.type == pygame.MOUSEBUTTONDOWN:
                result = self.ui.menu_click(event)
                if result == "start_game":
                    # self.start_combat()
                    self.state = "overworld"

        if self.turn_phase == "player":
            result = self.ui.click(event, self.player, self.enemy)
            if result == "end_turn":
                print("Player ended turn")
                self.turn_phase = "enemy"
                self.enemy_turn_pending = True

    def draw_game_over(self, message):
        font = pygame.font.SysFont("arial", 40)
        label = font.render(message, True, "white")
        self.window.blit(label, (200, 250))

    def start_combat(self):
        pygame.mixer.music.load("music/fight combat v1.mp3")
        pygame.mixer.music.play(-1)
        self.state = "playing"
        self.turn_phase = self.first_turn()
        self.first_turn_flag = True
        self.enemy_first_turn = True

        if self.turn_phase == "player":
            self.prepare_player_turn()
        else:
            self.enemy_turn_pending = True

    def check_damage(self):

        if self.player.health < self.player_current_health or self.enemy.health:
            return True
        else:
            return False



    def reset(self):
        self.state = "menu"
        self.player = Character("Player", "warrior", 100, 100, 0, ProtoDeck)
        self.enemy = Character("lesser punkin", "trickster", 50, 50, 0, EnemyDeck)
        self.enemy.sprite_path = "img/characters/punkin 1.png"
        self.player.sprite_path = "img/character png.png"
        self.ui = UIManager(self.window)
        self.enemy_turn_pending = False
        self.enemy_action_text = ""
        self.enemy_text_timer = 0
        self.turn_phase = self.first_turn()
        self.game_over = False
        self.first_turn_flag = True
        self.enemy_first_turn = True
        self.win_timer = 0
        self.music()  # Ensure music resets too

    def update(self):


        if self.state == "menu":
            self.music()

            self.ui.draw_menu()
            pygame.display.update()
            return
        if self.state == "game over":
            self.music()


            self.ui.draw_game_over()

            pygame.display.update()
            return

        if self.state == "playing":
            self.music()
            self.window.fill((0, 0, 0))
            # Clear screen

            # make sure enemy text displays on top

            if self.enemy_text_timer > 0:
                self.ui.draw_text(self.enemy_action_text, 0.7, 0.20, "red")
                self.enemy_text_timer -= 1

            #### BACKGROUND ###
            # win_w, win_h = self.window.get_size()
            # self.combat_background_scaled = pygame.transform.scale(self.combat_background, (win_w, win_h))
            # self.window.blit(self.combat_background_scaled, (0, 0))

            # Draw player UI
            self.ui.draw_character(self.player, 0.45, 0.25)
            self.ui.draw_character(self.enemy, 0.75, 0.25)

            self.ui.draw_health_bar(self.player, 0.05, 0.05)
            self.ui.draw_health_bar(self.enemy, 0.7, 0.05)
            self.ui.draw_text(f"{self.player.energy}", 0.05, 0.12, "yellow", size_ratio=0.025)
            self.ui.draw_text(f"{self.enemy.energy}", 0.7, 0.12, "yellow", size_ratio=0.025)
            self.ui.draw_text(f"{self.player.health} / {self.player.max_hp}", 0.05, 0.02, "green", size_ratio=0.025)
            self.ui.draw_text(f"{self.enemy.health} / {self.enemy.max_hp}", 0.70, 0.02, "green", size_ratio=0.025)

            self.ui.draw_energy_bar(self.player, 0.05, 0.1)
            self.ui.draw_energy_bar(self.enemy, 0.7, 0.1)

            self.ui.draw_dice(self.player)
            self.ui.draw_card_buttons(self.player.hand)
            self.ui.draw_reroll_button()
            self.ui.draw_sort_btn()
            # self.ui.draw_next_phase()


            # Draw enemy UI


            # Player phase buttons
            if self.turn_phase == "player":
                self.ui.draw_text(f"rerolls: {self.player.rerolls}", 0.05, 0.45, "red", size_ratio=0.03)
                #### todo update reroll count here somehow: i think its good


                # pygame.display.update()
                if self.ui.combo_amt:

                    self.ui.draw_text(self.ui.combo_amt, 0.4, 0.15, "green", size_ratio=0.04)

                if self.ui.current_button == "next":
                    self.ui.clear_button_area()
                    self.ui.draw_next_phase()
                elif self.ui.current_button == "end":
                    self.ui.clear_button_area()
                    self.ui.end_turn()
                    # if self.player_dealt_damage():

                self.ui.show_card_hover()

                pygame.display.update()

            # Run enemy turn once
            if self.enemy_turn_pending:
                self.enemy_turn()
                self.enemy_turn_pending = False





            if self.player.health <= 0:
                self.game_over = True
                self.draw_game_over("You lost!")
                self.win_timer += 1
                if self.win_timer >= 80:
                    self.state = "game over"
                    self.win_timer = 0


                    pygame.display.update()

                    return

            elif self.enemy.health <= 0:
                self.game_over = True
                self.draw_game_over("You won!")
                self.player_tokens.append(self.punkin_token)
                self.punkin_defeated = True
                self.win_timer += 1
                if self.win_timer >= 20:

                    self.win_timer = 0
                    self.state = "overworld"

                    # reset for next time




                pygame.display.update()
                return

 #################### OVERWORLD DIALOGUE and other stuff ######################
        if self.state == "overworld":
            self.music()
            self.keys = pygame.key.get_pressed()

            ### statue info ##
            if self.overworld.sign_timer > 0:
                self.overworld.draw()
                self.overworld.signs()
                pygame.display.update()
                self.overworld.sign_timer -= 1
                return  # Prevent movement while sign is showing

            # Trigger dialogue with Space key while colliding
            if self.overworld.check_collision() and self.keys[pygame.K_SPACE] and not self.dialogue_triggered:
                if self.punkin_defeated:
                    self.overworld.dialogue_response = "defeated"
                    self.overworld.dialogue_timer = 30
                    self.dialogue_triggered = True
                    self.dialogue_active = False
                else:
                    self.dialogue_active = True
                    self.dialogue_triggered = True

            if self.overworld.dialogue_response == "defeated":
                self.overworld.draw()
                self.overworld.display_info(punkin_defeated=True)
                pygame.display.update()

                if self.overworld.dialogue_timer > 0:
                    self.overworld.dialogue_timer -= 1
                else:
                    self.overworld.dialogue_response = None  # ✅ Clear the message
                    self.dialogue_active = False
                    self.dialogue_triggered = False  # ✅ Allow retriggering later
                return

            # Handle "ah man..." response
            if self.overworld.dialogue_response == "no":
                self.overworld.draw()
                self.overworld.display_info(punkin_defeated=self.punkin_defeated)
                pygame.display.update()

                if self.overworld.dialogue_timer > 0:
                    self.overworld.dialogue_timer -= 1
                else:
                    self.overworld.dialogue_response = None
                    self.dialogue_active = False
                    self.dialogue_triggered = True
                return  # Prevent movement during countdown

            # Show initial dialogue box
            if self.dialogue_active:
                self.overworld.draw()
                self.overworld.display_info(punkin_defeated=self.punkin_defeated)
                pygame.display.update()
                return  # Prevent movement while dialogue is active

            # Handle "yes" response and start combat
            if self.dialogue_result == "yes":
                self.dialogue_result = None
                self.dialogue_active = False

                if not self.punkin_defeated:
                    self.dialogue_triggered = False
                    self.window.fill((0, 0, 0))
                    self.start_combat()
                    pygame.display.update()
                    return

            # Reset trigger if player walks away
            if not self.overworld.check_collision():
                self.dialogue_triggered = False


            # Normal overworld flow
            self.overworld.process_input(self.keys)
            self.overworld.update_walk_animation()  # ✅ move this up
            self.overworld.draw()
            pygame.display.update()

        elif self.state == "credits":
            print("rolling credits")
            self.music()
            self.sm.play_credits(self.window)
            pygame.display.update()








