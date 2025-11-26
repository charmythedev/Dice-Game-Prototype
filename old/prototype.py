import pygame
import random
from managers.ui_manager import UIManager
from managers.game_manager import GameManager

#todo finish character, deck, dice, and card logic
#todo create pygame window
#todo create random enemy actions
#todo put everything on pygame window, buttons for dice, buttons for actions, health bars, energy bar, etc.

#------------------------------------------- UI ---------------------------------------------------------------#

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('../fight combat v1.wav')

#
# player = Character('Trevor', "Gambler", 100,100, ProtoDeck)
# enemy = Character('Thug', "enemy", 30,30, ProtoDeck)

window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('Dice Game Prototype')
ui = UIManager(window)
running = True


player_cards = player.deck.build_deck()
random.shuffle(player_cards)
hand = player_cards[:5]


pygame.mixer.music.play(-1)  # Should be outside loop or called once before loop
gm = GameManager(window)
player.roll_dice()
while running:

    window.fill("purple")

    ui.draw_reroll_button()

    ui.draw_health_bar(player, 50, 50)
    ui.draw_health_bar(enemy, 550, 50)
    ui.draw_energy_bar(player, 50, 80)
    ui.draw_card_buttons(hand, 50, 400)
    ui.show_card_hover()
    if ui.current_button == "next":
        ui.draw_next_phase()

    elif ui.current_button == "end":

        ui.end_turn()





    ui.draw_dice(player, 50, 200)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ui.click(event, player, enemy)

    pygame.display.update()
    clock.tick(60)




#------------------------------------------- Character setup ---------------------------------------------------#

#------------------------------------------- Initiative --------------------------------------------------------#
# def enemy_start():
#
#     return f"{enemy.name} goes first"
#
# def char_start():
#     return f"{player.name} goes first"

    #
    # char_roll = random.randint(1,6)
    # enemy_roll = random.randint(1,6)
    #
    # if char_roll < enemy_roll:
    #     print(enemy_start())
    # else:
    #     print(char_start())



    #------------------------------------------- Draw First Hand --------------------------------------------------#






    #------------------------------------------- roll/energy -------------------------------------------------------#
    # player.roll_dice()
    #------------------------------------------- play cards -------------------------------------------------------#
    # for card in hand:
    #     print(card)
    # while True:
    #     card_index = int(input("which card would you like to play (ex. 1)?")) -1
    #     selected_card = hand[card_index]
    #     if player.energy >= selected_card.cost:
    #         print(f"Playing {selected_card.name} for {selected_card.cost} energy")
    #         player.energy -= selected_card.cost
    #
    #     else:
    #         print("Not enough energy to play that card!")
    #
    #     input("end turn? y/n")
    # ------------------------------------------ check damage -----------------------------------------------------#

    # ------------------------------------------ enemy turn -------------------------------------------------------#


# clock.tick(60)

pygame.quit()