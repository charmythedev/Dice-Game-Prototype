import pygame
class Card:
    def __init__(self, name, card_type, effect, value, cost, synergy, art_path):
        self.name = name
        self.card_type = card_type
        self.effect = effect
        self.cost = cost
        self.synergy = synergy
        self.value = value
        self.art_path = art_path
        if art_path:
            try:
                self.art = pygame.image.load(art_path).convert_alpha()
            except Exception as e:
                print(f"Failed to load art for {self.name}: {e}")
                self.art = None
        else:
            self.art = None

    def __repr__(self):
        return f'{self.name} {self.card_type} {self.effect} {self.cost}'
