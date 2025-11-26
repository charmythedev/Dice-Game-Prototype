import random
from collections import Counter
import math
from managers.card import Card

from managers.deck import ProtoDeck


# from managers.deck import Deck

## todo: determine what exactly a character can do
## todo: create subclasses, levels? xp?
## todo: draw cards, roll dice, play cards, and make these affect enemy or game logic

class Character:
    def __init__(self, name, subclass, health, max_hp, defense, deck):
        self.name = name
        self.subclass = subclass
        self.energy = 0
        self.health = health
        self.max_hp = max_hp
        self.max_energy = 100
        self.deck = deck()
        self.hand = []
        self.rolls =[]
        self.sprite_path = None
        self.draw_bonus = 0
        self.defense = defense
        self.base_rerolls = 2
        self.rerolls = self.base_rerolls
        self.bonus_rerolls = 0
        self.bonus_energy = 0

        self.combo_synergy = ""

        self.max_hand_size = 5

    def draw_cards(self, amount):
        if not self.deck.cards:
            self.deck.reshuffle()

        drawn = 0
        while drawn < amount and self.deck.cards and len(self.hand) < self.max_hand_size:
            card = self.deck.cards.pop()
            self.hand.append(card)
            # self.deck.discard_pile.append(card)
            drawn += 1

        if len(self.hand) >= self.max_hand_size:
            print("Hand is full")

    def roll_dice(self):

        self.rolls = [random.randint(1, 6) for _ in range(5)]

        print(f"Initial rolls: {self.rolls}")


    def check_combo(self, rolls):

        counts = Counter(rolls).values()
        sorted_unique = sorted(set(rolls))

        # Check for large straight (5 consecutive numbers)
        if any(all(num + i in sorted_unique for i in range(5)) for num in range(1, 3)):
            combo = (35, "large straight")
            self.combo_synergy = combo[1]
            return combo

        # Check for small straight (4 consecutive numbers)
        if any(all(num + i in sorted_unique for i in range(4)) for num in range(1, 4)):
            combo = (15, "small straight")
            self.combo_synergy = combo[1]
            return combo

        if 5 in counts:
            print("Yahtzee!")
            combo = (50, "5 of a kind")
            self.combo_synergy = combo[1]
            return combo
        elif 4 in counts:
            combo = (40, "4 of a kind")
            self.combo_synergy = combo[1]
            return combo
        elif 3 in counts and 2 in counts:
            combo = (30, "full house")
            self.combo_synergy = combo[1]
            return combo
        elif 3 in counts:
            combo = (25, "3 of a kind")
            self.combo_synergy = combo[1]
            return combo
        elif list(counts).count(2) == 2:
            combo = (20, "two pair")
            self.combo_synergy = combo[1]
            return combo

        elif 2 in counts:
            combo =(10, "pair")
            self.combo_synergy = combo[1]
            return combo

        ###todo add sm and large straight




        else:
            return (0, "none")

    def calc_energy(self,rolls, score):
        energy_gained = sum(rolls) + math.floor(score/2)

        self.energy += energy_gained + self.bonus_energy
        return energy_gained

    def activate_card(self, card, enemy):
        if card in self.hand and self.energy >= card.cost:
            self.energy -= card.cost
            self.hand.remove(card)
            self.deck.discard_pile.append(card)
            if card.synergy.strip().lower() == self.combo_synergy.strip().lower():

                card.value *= 2
                print(f"Synergy activated for {card.name}! New value: {card.value}")


            if card.card_type == "attack":
                damage = max(0, card.value - enemy.defense)
                enemy.health -= damage
                print(f"damage dealt:{damage}")

            if card.card_type == "heal":
                self.health = min(self.max_hp, self.health + card.value)
                print("")
            if card.card_type == "buff":
                pass  # Add buff logic here
            if card.card_type == "defense":
                self.defense += card.value
                print(f"defense:{self.defense}")
            if card.card_type == "spell":
                pass
            if card.name.lower() == "focus":
                self.draw_bonus += 2
                print(f"{self.name} gained draw bonus: {self.draw_bonus}")
            if card.name.lower() == "lucky rabbit's foot":
                self.bonus_rerolls += 1
                print(self.rerolls)
            if card.name.lower() == "meditate":
                self.bonus_energy += card.value
                print(f"meditate activated: bonus energy: {self.bonus_energy}")

            return True
        return False




