# import random
from managers.card import Card


class ProtoDeck:
    def __init__(self):
        self.cards = self.build_deck()
        self.discard_pile = []

        ##todo define cards, what they do and how they work with dice rolls
        # todo fix deck to actually be random

        # as a basic we'll make a block and a Whack each costing some amount of energy
    def build_deck(self):
        return [
            Card("Whack", "attack", "Deal 5 damage", 10, 10, "pair", "img/cards/whack unfinished.png"),
            Card("Whack", "attack", "Deal 5 damage", 10, 10, "pair", "img/cards/whack unfinished.png"),
            Card("Whack", "attack", "Deal 5 damage", 10, 10, "pair", "img/cards/whack unfinished.png"),
            Card("Guard", "defense", "Gain 5 armor", 5, 10, "pair", "img/cards/guard unfinished.png"),
            Card("Guard", "defense", "Gain 5 armor", 5, 10, "pair", "img/cards/guard unfinished.png"),
            Card("Heal", "heal", "Restore 5 HP", 5, 8, "pair", "img/cards/heal unfinished.png"),
            Card("Fireball", "attack", "Deal 15 damage", 8, 13, "3 of a kind", "img/fireball card 1.png"),
            Card("Fireball", "attack", "Deal 15 damage", 8, 13, "3 of a kind", "img/fireball card 1.png"),
            Card("Focus", "spell", "Draw 2 cards next turn", 2, 10, "two pair", r"img/cards/Focus 1.png"),
            Card("Meditate", "spell", "gain an extra 5 energy next turn", 3, 0, "3 of a kind",
                 "img/cards/meditate bad.png"),
            Card("Lucky Rabbit's Foot", "relic", " one extra reroll next turn", 1, 10, "5 of a kind",
                 "img/cards/lucky rabbit's foot precursor.png")
        ] * 2

            ####unfinished return later
    def reshuffle(self):
        self.cards = self.build_deck()
class EnemyDeck:
    def __init__(self):
        self.cards = self.build_deck()
        self.discard_pile = []

    def build_deck(self):
        return [
            Card("Whack", "attack", "Deal 5 damage", 5, 10, "pair", ""),
            Card("Punkin Bomb", "attack", "Deal 10 damage", 5, 15, "3 of a kind", ""),
            Card("Whack", "attack", "Deal 5 damage", 5, 5, "pair", ""),

        ] * 4

        ####unfinished return later

    def reshuffle(self):
        self.cards = self.build_deck()



