import pygame

class SceneManager:
    def __init__(self, window):

        self.win_x, self.win_y = window.get_size()
        self.state = "credits"
        self.frames = []
        for i in range(1, 13):
            frame = pygame.image.load(
                f"animation/cliff_scene/cliff scene purp{i}.png"
            ).convert_alpha()
            self.frames.append(pygame.transform.scale(frame, (self.win_x, self.win_y)))
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 10  # how many ticks before switching frame

    def play_credits(self, window):
        # increment timer
        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.anim_timer = 0

        # draw current frame
        current_frame = self.frames[self.frame_index]
        window.blit(current_frame, (0, 0))