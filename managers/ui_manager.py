import pygame
import random

from managers.character_class import Character


class UIManager:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont("arial", 20)
        self.selected_dice = []
        self.dice_rects = []
        self.card_buttons = []

        self.shaking = False
        self.shake_timer = 0
        self.shake_duration = 10
        self.shake_offset = 10

        self.current_button = "next"
        self.combo_amt = ""

        ######### layout ##########

        self.original_layout = {
            "next_button": pygame.Rect(175, 300, 100, 30),
            "end_turn_butt": pygame.Rect(175, 300, 100, 30),
            "start_button_rect": pygame.Rect(250, 400, 200, 60),
            "reroll_rect": pygame.Rect(50, 300, 100, 30),
            "card_start": (50, 400),
            "dice_start": (50, 120),
        }

        ### todo move this into diff class for energy gain
        ###todo move anything that does damage, energy or whatever calc outside of the scope of this class
        ## todo this class is for drawing ui only
        ## todo and possibly only combat ui not overworld

        self.setup_buttons()
        self.start_button_rect = pygame.Rect(250, 400, 200, 60)

        ######################################## menu  ###########################################################################################
        self.moon_frames = []
        for i in range(1,8):
            frame = pygame.image.load(f"animation/crescent proto hd{i}.png").convert_alpha()
            self.moon_frames.append(frame)
        self.moon_frame_index = 0
        self.moon_anim_timer = 0

        ######################################## game over #############################################################################################

        self.go_frames = []
        for i in range(1,27):
            go_frame = pygame.image.load(f"animation/game_over/gameover{i}.png").convert_alpha()
            self.go_frames.append(go_frame)
        self.go_frame_index = 0
        self.go_anim_timer = 0

    def draw_menu(self):
        win_w, win_h = self.window.get_size()
        self.window.fill((0, 0, 0))

        # Animate moon sprite
        self.moon_anim_timer += 1
        if self.moon_anim_timer >= 9:
            self.moon_frame_index = (self.moon_frame_index + 1) % len(self.moon_frames)
            self.moon_anim_timer = 0

        moon_sprite = self.moon_frames[self.moon_frame_index]
        moon_scaled = pygame.transform.scale(moon_sprite, (win_w, win_h))
        self.window.blit(moon_scaled, (0, 0))

        # Draw start button dynamically
        button_w, button_h = int(win_w * 0.25), int(win_h * 0.1)
        button_x, button_y = int(win_w * 0.375), int(win_h * 0.75)
        self.start_button_rect = pygame.Rect(button_x, button_y, button_w, button_h)




    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            return "start_game"

    def draw_game_over(self):
        win_w, win_h = self.window.get_size()
        self.window.fill((0, 0, 0))

        self.go_anim_timer += 1
        if self.go_anim_timer >= 8:
            self.go_frame_index = (self.go_frame_index + 1) % len(self.go_frames)
            self.go_anim_timer = 0

        go_sprite = self.go_frames[self.go_frame_index]
        go_scaled = pygame.transform.scale(go_sprite, (win_w, win_h))
        self.window.blit(go_scaled, (0, 0))

        # Optional: overlay text
        # font = pygame.font.SysFont("arial", int(win_h * 0.08))
        # label = font.render("Game Over", True, "white")
        # self.window.blit(label, (int(win_w * 0.35), int(win_h * 0.1)))
    def draw_character(self, character, anchor_x_ratio, anchor_y_ratio):
        win_w, win_h = self.window.get_size()
        sprite_w, sprite_h = int(win_w * 0.25), int(win_h * 0.25)
        x = int(win_w * anchor_x_ratio)
        y = int(win_h * anchor_y_ratio)

        if character.sprite_path:
            sprite = pygame.image.load(character.sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (sprite_w, sprite_h))
            self.window.blit(sprite, (x, y))
        else:
            fallback_w, fallback_h = int(win_w * 0.1), int(win_h * 0.15)
            pygame.draw.rect(self.window, "darkgray", (x, y, fallback_w, fallback_h))
            self.draw_text(character.name, x + 10, y + 10, "white")

    def setup_buttons(self):
        win_w, win_h = self.window.get_size()

        # Button size and position
        button_w = int(win_w * 0.125)
        button_h = int(win_h * 0.05)
        button_x = int(win_w * 0.25)
        button_y = int(win_h * 0.75)

        self.next_button = pygame.Rect(button_x, button_y, button_w, button_h)
        self.end_turn_butt = pygame.Rect(button_x, button_y, button_w, button_h)

    def draw_health_bar(self, character, anchor_x_ratio, anchor_y_ratio):
        win_w, win_h = self.window.get_size()
        bar_w, bar_h = int(win_w * 0.25), int(win_h * 0.03)
        x = int(win_w * anchor_x_ratio)
        y = int(win_h * anchor_y_ratio)

        hp_ratio = character.health / character.max_hp
        pygame.draw.rect(self.window, "red", (x, y, bar_w, bar_h))
        pygame.draw.rect(self.window, "green", (x, y, int(bar_w * hp_ratio), bar_h))

    def draw_energy_bar(self, character, anchor_x_ratio, anchor_y_ratio):
        win_w, win_h = self.window.get_size()
        bar_w, bar_h = int(win_w * 0.2), int(win_h * 0.02)
        x = int(win_w * anchor_x_ratio)
        y = int(win_h * anchor_y_ratio)

        energy_ratio = min(character.energy / character.max_energy, 1)
        pygame.draw.rect(self.window, "gray", (x, y, bar_w, bar_h))
        pygame.draw.rect(self.window, "yellow", (x, y, int(bar_w * energy_ratio), bar_h))


    def draw_text(self, text, anchor_x, anchor_y, color="white", size_ratio=0.03, center=False):
        win_w, win_h = self.window.get_size()
        font_size = max(12, int(win_h * size_ratio))  # Prevent font from getting too small
        font = pygame.font.SysFont("arial", font_size)
        label = font.render(text, True, color)

        x = int(win_w * anchor_x)
        y = int(win_h * anchor_y)

        if center:
            x -= label.get_width() // 2
            y -= label.get_height() // 2

        self.window.blit(label, (x, y))


    def draw_card_buttons(self, hand):
        win_w, win_h = self.window.get_size()

        # Fixed card size for consistency across resolutions
        card_w, card_h = int(120), int(190)

        num_cards = len(hand)
        total_card_width = num_cards * card_w
        available_space = win_w - total_card_width

        # Calculate spacing between cards
        spacing = max(20, available_space // (num_cards + 1))

        # Center the row of cards
        start_x = (win_w - (num_cards * card_w + (num_cards - 1) * spacing)) // 2
        start_y = int(win_h * 0.7)

        self.card_buttons = []

        for i, card in enumerate(hand):
            x = start_x + i * (card_w + spacing)
            rect = pygame.Rect(x, start_y, card_w, card_h)
            self.card_buttons.append((card, rect))

            if hasattr(card, "art") and card.art:
                scaled_art = pygame.transform.scale(card.art, (card_w, card_h))
                self.window.blit(scaled_art, rect)
            else:
                pygame.draw.rect(self.window, "blue", rect)
                self.draw_text(card.name, rect.x + 10, rect.y + 10)
    def clear_button_area(self):
        pygame.draw.rect(self.window, self.window.get_at((0, 0)), (0, 0, 0, 0))

    def show_card_hover(self):

        mouse_pos = pygame.mouse.get_pos()
        for card, rect in self.card_buttons:
            if rect.collidepoint(mouse_pos):
                if hasattr(card, "art") and card.art:
                    scaled_art = pygame.transform.scale(card.art, (300, 450))
                    self.window.blit(scaled_art, (rect.x, rect.y - 360))

                # effect = card.effect
                #
                # cost = card.cost
                # hover_text = f"{card.name}: {effect}, Cost: {cost}, Synergy:{card.synergy}"
                # self.draw_text(hover_text, rect.x, rect.y - 25, color="yellow")
                break  # Only show one hover at a time

    def sort_rolls(self, character):
        return sorted(character.rolls)

    def draw_sort_btn(self):
        win_w, win_h = self.window.get_size()

        # Anchor-based position (e.g. 0.4 across, 0.76 down)
        anchor_x = 0.375
        anchor_y = 0.21

        button_w = int(win_w * 0.08)
        button_h = int(win_h * 0.05)
        x = int(win_w * anchor_x)
        y = int(win_h * anchor_y)

        self.sort_button = pygame.Rect(x, y, button_w, button_h)
        pygame.draw.rect(self.window, "yellow", self.sort_button)
        self.draw_text("sort", anchor_x + 0.0195, anchor_y + 0.01, "black")

    def click(self, event, character, enemy):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Dice selection
            for i, rect in enumerate(self.dice_rects):
                if rect.collidepoint(mouse_pos):
                    if i in self.selected_dice:
                        self.selected_dice.remove(i)
                    else:
                        self.selected_dice.append(i)
            ## sort button
            if hasattr(self, 'sort_button') and self.sort_button.collidepoint(mouse_pos):
                character.rolls = self.sort_rolls(character)
                return "sorted"

            # Reroll button
            if hasattr(self, 'reroll_rect') and self.reroll_rect.collidepoint(mouse_pos):
                self.reroll_dice(character)
                return "reroll"

            # ✅ NEXT button logic
            if self.current_button == "next" and self.next_button.collidepoint(mouse_pos):
                combo_score, combo_synergy = character.check_combo(character.rolls)
                character.calc_energy(character.rolls, combo_score)
                self.combo_amt = f"{combo_synergy} (+{combo_score} energy)"
                self.clear_button_area()
                self.current_button = "end"
                return None

            # ✅ END TURN button logic
            if self.current_button == "end" and self.end_turn_butt.collidepoint(mouse_pos):
                self.clear_button_area()
                self.current_button = "next"
                return "end_turn"

            # ✅ Card logic (only if in "end" phase)
            for card, rect in self.card_buttons:
                if self.current_button == "end" and rect.collidepoint(mouse_pos):
                    combo_synergy, _ = character.check_combo(character.rolls)
                    if character.activate_card(card, enemy):
                        self.card_buttons.remove((card, rect))
                        self.clear_button_area()
                        self.draw_card_buttons(character.hand)
                        print(f"Played {card.name}, cost {card.cost}")
                    else:
                        print("Not enough energy")
                    break

    def draw_dice(self, character):
        win_w, win_h = self.window.get_size()
        dice_size = int(win_w * 0.05)
        start_x = int(win_w * 0.05)
        start_y = int(win_h * 0.2)

        self.dice_rects = []

        for i, die in enumerate(character.rolls):
            x = start_x + i * (dice_size + 10)
            rect = pygame.Rect(x, start_y, dice_size, dice_size)
            self.dice_rects.append(rect)

            # Highlight if selected
            color = "lightblue" if i in self.selected_dice else "white"
            pygame.draw.rect(self.window, color, rect)

            # Centered number
            font_size = max(12, int(win_h * 0.04))
            font = pygame.font.SysFont("arial", font_size)
            label = font.render(str(die), True, "black")
            label_x = rect.x + (rect.width - label.get_width()) // 2
            label_y = rect.y + (rect.height - label.get_height()) // 2
            self.window.blit(label, (label_x, label_y))

    def draw_reroll_button(self):
        win_w, win_h = self.window.get_size()

        # Button size and position
        button_w = int(win_w * 0.125)
        button_h = int(win_h * 0.05)
        button_x = int(win_w * 0.05)
        button_y = int(win_h * 0.35)

        self.reroll_rect = pygame.Rect(button_x, button_y, button_w, button_h)
        pygame.draw.rect(self.window, "orange", self.reroll_rect)

        # Centered label inside button
        font_size = max(12, int(win_h * 0.035))
        font = pygame.font.SysFont("arial", font_size)
        label = font.render("REROLL", True, "red")
        label_x = button_x + (button_w - label.get_width()) // 2
        label_y = button_y + (button_h - label.get_height()) // 2
        self.window.blit(label, (label_x, label_y))

    def reroll_dice(self, character):
        if character.rerolls > 0 and self.selected_dice:

            for i in self.selected_dice:
                character.rolls[i] = random.randint(1, 6)
            self.selected_dice.clear()
            character.rerolls -= 1
        #todo move this function into character and pass in to ui.drawdice

    def draw_next_phase(self):
        win_w, win_h = self.window.get_size()

        # Button size and position
        button_w = int(win_w * 0.125)
        button_h = int(win_h * 0.05)
        button_x = int(win_w * 0.25)  # aligned near reroll button
        button_y = int(win_h * 0.35)

        self.next_button = pygame.Rect(button_x, button_y, button_w, button_h)
        pygame.draw.rect(self.window, "red", self.next_button)

        # Centered label inside button
        font_size = max(12, int(win_h * 0.035))
        font = pygame.font.SysFont("arial", font_size)
        label = font.render("ATTACK PHASE", True, "white")
        label_x = button_x + (button_w - label.get_width()) // 2
        label_y = button_y + (button_h - label.get_height()) // 2
        self.window.blit(label, (label_x, label_y))

    def end_turn(self):
        win_w, win_h = self.window.get_size()

        # Button size and position
        button_w = int(win_w * 0.125)
        button_h = int(win_h * 0.05)
        button_x = int(win_w * 0.25)  # right of attack phase button
        button_y = int(win_h * 0.35)

        self.end_turn_butt = pygame.Rect(button_x, button_y, button_w, button_h)
        pygame.draw.rect(self.window, "green", self.end_turn_butt)

        # Centered label inside button
        font_size = max(12, int(win_h * 0.035))
        font = pygame.font.SysFont("arial", font_size)
        label = font.render("END TURN", True, "white")
        label_x = button_x + (button_w - label.get_width()) // 2
        label_y = button_y + (button_h - label.get_height()) // 2
        self.window.blit(label, (label_x, label_y))


    def start_shake(self):
        self.shaking = True
        self.shake_timer = 0

    def update_shake(self, sprite, x, y):
        if self.shaking:
            offset = self.shake_offset if self.shake_timer % 2 == 0 else -self.shake_offset
            self.window.blit(sprite, (x+offset, y))
            self.shake_timer += 1
            if self.shake_timer >= self.shake_duration:
                self.shaking = False
        else:
            self.window.blit(sprite, (x, y))
