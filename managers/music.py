import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dice Game")
clock = pygame.time.Clock()
running = True
pygame.mixer.music.load('../music/vg soundtrack town.wav')
pygame.mixer.music.play(-1)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            screen.fill((0,0,0))
            pygame.display.update()
