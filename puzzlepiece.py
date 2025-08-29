import pygame as pg
from globalSurfaces import PUZZLE_PIECE, ACHIEVE_PUZZLE_SOUND


class PuzzlePiece:
    def __init__(self, x, y, color, rotation=0):
        self.image: pg.Surface = PUZZLE_PIECE.copy()
        self.image.fill(
            color + [255], special_flags=pg.BLEND_RGBA_MIN
        )  # tint the black puzzle piece with the given color (keeping alpha)
        self.image = pg.transform.rotate(self.image, rotation)
        self.rect: pg.Rect = self.image.get_rect(topleft=(x, y))
        self.collected: bool = False
        self.playing_fade_animation: bool = False

    def draw(self, surface: pg.Surface):
        if not self.collected and not self.playing_fade_animation:
            surface.blit(self.image, self.rect)

        if self.playing_fade_animation:

            self.fade_alpha -= 5
            self.fade_size = (self.fade_size[0] - 5, self.fade_size[1] - 5)
            fade_image = pg.transform.scale(self.image, self.fade_size)
            fade_image.set_alpha(self.fade_alpha)
            fade_rect = fade_image.get_rect(center=self.rect.center)
            surface.blit(fade_image, fade_rect)

            if self.fade_alpha <= 0:

                self.fade_alpha = 0
                self.playing_fade_animation = False
                self.collected = True

    def collect(self):

        self.playing_fade_animation = True
        self.fade_alpha = 255
        self.fade_size = self.image.get_size()
        ACHIEVE_PUZZLE_SOUND.play()
