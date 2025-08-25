from time import time
from globalSurfaces import BUTTON_DOWN, BUTTON_UP
import pygame as pg


class Button:
    def __init__(self, rect : pg.Rect, text='', text_color=(0, 0, 0), font_size=30):
        self.surf = BUTTON_UP
        self.rect = self.surf.get_rect(topleft=rect.topleft)
        self.state = 'UP'
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font = pg.font.SysFont("Arial", self.font_size)
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=(self.rect.center[0], self.rect.center[1]- 50))
        self.last_pressed_time = None

    def draw(self, surface : pg.Surface):
        surface.blit(self.surf, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        if event.type == pg.USEREVENT + 0 and self.rect.collidepoint(event.pos):
            self.last_pressed_time = time()
            return True
        return False

    def handle_event(self, event):
        if self.is_clicked(event):
            self.state = 'DOWN'
            self.surf = BUTTON_DOWN
            # TODO: play sound effect

        if event.type == pg.USEREVENT + 1:  # Reset event
            self.reset()

    def reset(self):
        self.state = 'UP'
        self.surf = BUTTON_UP