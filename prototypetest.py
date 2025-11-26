import pygame
from managers.ui_manager import UIManager
from managers.game_manager import  GameManager


#------------------------------------------- UI ---------------------------------------------------------------#

pygame.init()



fullscreen = False

window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption('Dice Game Prototype')

running = True



gm = GameManager(window)
ui = UIManager(window)




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        gm.handle_click(event)
        if event.type == pygame.VIDEORESIZE:
            new_size = event.size
            new_window = pygame.display.set_mode(new_size, pygame.RESIZABLE)

    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # print(f"Cursor position: ({mouse_x}, {mouse_y})")
    #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        if gm.state == "overworld" and gm.dialogue_active and not gm.punkin_defeated:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(gm.overworld, "yes_button") and gm.overworld.yes_button.collidepoint(event.pos):
                    gm.dialogue_result = "yes"
                    gm.dialogue_active = False
                elif gm.overworld.no_button.collidepoint(event.pos):
                    gm.dialogue_result = "no"
                    gm.overworld.dialogue_response = "no"
                    gm.overworld.dialogue_timer = 60
                    gm.dialogue_active = False
        if gm.state == "overworld" and gm.punkin_defeated:
            gm.overworld.dialogue_timer = 30
            if gm.overworld.dialogue_timer >= 0:
                gm.dialogue_active = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if gm.state == "overworld" and gm.overworld.check_statue_collision():
                gm.overworld.sign_timer = 60
        if gm.state == "overworld" and gm.punkin_defeated:
            gm.state = "credits"


    gm.update()
    clock.tick(60)

pygame.quit()