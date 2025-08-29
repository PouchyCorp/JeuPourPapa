import pygame as pg
from globalSurfaces import PLAYER_ANIMATION


class Player:
    def __init__(self, x, y):
        self.anim = PLAYER_ANIMATION
        self.surf = self.anim.get_frame()
        self.anim.reset_frame()
        self.idle_surf = self.surf.copy()
        self.rect = pg.Rect(x, y, self.surf.get_width(), self.surf.get_height())
        self.moving = False
        self.facing_left = False

    def draw(self, surface: pg.Surface):
        surface.blit(self.surf, self.rect)

    def handle_movement_inputs(self):
        self.moving = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= 5
            self.moving = True
            self.facing_left = True
        if keys[pg.K_RIGHT]:
            self.rect.x += 5
            self.moving = True
            self.facing_left = False
        if keys[pg.K_UP]:
            self.rect.y -= 5
            self.moving = True
        if keys[pg.K_DOWN]:
            self.rect.y += 5
            self.moving = True

    def handle_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                pg.event.custom_type = pg.USEREVENT + 0
                pg.event.post(
                    pg.event.Event(
                        pg.event.custom_type,
                        {"pos": (self.rect.centerx, self.rect.bottom - 20)},
                    )
                )

    def update(self):
        if self.moving:
            self.surf = self.anim.get_frame()
        else:
            self.anim.reset_frame()
            self.surf = self.idle_surf.copy()  # Use copy to avoid modifying original

        # Flip sprite based on direction
        if not self.facing_left:
            self.surf = pg.transform.flip(self.surf, True, False)
