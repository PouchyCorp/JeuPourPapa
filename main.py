import math


class Game:
    def __init__(self, display):
        pg.init()
        self.screen: pg.Surface = display
        pg.display.set_caption("TOP SECRET")
        self.clock = pg.time.Clock()
        self.fade = sprite.ScreenFade()

        self.player = Player(400, 300)
        self.level = 0
        self.running = True
        self.origin = (410, 0)
        self.secret_activated = False
        self.secret_timer = 0

        from globalSurfaces import ACHIEVE_LEVEL_SOUND

        self.ACHIEVE_LEVEL_SOUND = ACHIEVE_LEVEL_SOUND

        # Initialize starfield background
        from starfield import Starfield

        self.starfield = Starfield(
            self.screen.get_width(), self.screen.get_height(), num_stars=120
        )

    def init_level(self, level_ind: int):
        self.original_background = LEVELS[level_ind].background
        self.background = self.original_background.subsurface(
            (max(0, self.original_background.get_rect().centerx - 550), 0, 1100, 1100)
        )
        side_without_bitoniau = 550
        bitoniau = 88
        piece_size = (side_without_bitoniau, side_without_bitoniau)
        self.puzzle_pieces = [
            (
                PuzzlePiece(*self.origin, [162, 112, 112], rotation=0),
                pg.Rect(self.origin, piece_size),
            ),
            (
                PuzzlePiece(
                    self.origin[0] + side_without_bitoniau,
                    self.origin[1],
                    [171, 148, 124],
                    rotation=270,
                ),
                pg.Rect(
                    (self.origin[0] + side_without_bitoniau, self.origin[1]), piece_size
                ),
            ),
            (
                PuzzlePiece(
                    self.origin[0],
                    self.origin[1] + side_without_bitoniau - bitoniau,
                    [155, 179, 147],
                    rotation=90,
                ),
                pg.Rect(
                    (self.origin[0], self.origin[1] + side_without_bitoniau), piece_size
                ),
            ),
            (
                PuzzlePiece(
                    self.origin[0] + side_without_bitoniau - bitoniau,
                    self.origin[1] + side_without_bitoniau,
                    [160, 185, 190],
                    rotation=180,
                ),
                pg.Rect(
                    (
                        self.origin[0] + side_without_bitoniau,
                        self.origin[1] + side_without_bitoniau,
                    ),
                    piece_size,
                ),
            ),
        ]

        boundaries = []
        for i in range(4):
            boundaries.append(
                pg.Rect(
                    (
                        self.origin[0] + side_without_bitoniau * (i % 2),
                        self.origin[1] + side_without_bitoniau * (i // 2),
                    ),
                    (side_without_bitoniau, side_without_bitoniau),
                )
            )

        self.puzzle_manager = PuzzleManager(
            boundaries, self.puzzle_pieces, LEVELS[level_ind].minigames
        )

    def run(self):
        import start

        start.run(self.clock, self.screen)
        self.fade.start(0.012, start=math.pi / 2)  # Fade in at start
        while self.level < len(LEVELS) and self.running:
            self.finished_level = False
            self.init_level(self.level)
            while not self.finished_level and self.running:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)

            if self.finished_level:
                self.ACHIEVE_LEVEL_SOUND.play()
                self.animate_background_grow()

            self.fade.start(0.012, start=math.pi / 2)  # Fade out at end of level

            self.level += 1
        pg.quit()

    def handle_events(self):
        self.player.handle_movement_inputs()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            # Enhanced secret keybind to complete level: Ctrl+Shift+C
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    keys = pg.key.get_pressed()
                    if keys[pg.K_LCTRL] and keys[pg.K_LSHIFT]:
                        if not self.finished_level:
                            self.finished_level = True

            self.puzzle_manager.handle_event(event)

            self.player.handle_events(event)

    def update(self):
        self.player.update()
        self.puzzle_manager.update()
        if self.puzzle_manager.is_all_pieces_collected():
            self.finished_level = True
        self.starfield.update()
        self.fade.update()

    def draw(self):
        # Draw black space background with stars
        self.screen.fill((0, 0, 0))  # Black space
        self.starfield.draw(self.screen)  # Draw animated stars

        self.screen.blit(self.background, self.origin)
        self.puzzle_manager.draw(self.screen)
        self.player.draw(self.screen)

        # show fps
        fps = int(self.clock.get_fps())
        font = pg.font.SysFont("Arial", 30)
        fps_surf = font.render(f"FPS: {fps}", True, (255, 0, 255))
        self.screen.blit(fps_surf, (10, 10))

        self.fade.draw(self.screen)

        pg.display.flip()

    def animate_background_grow(self):
        grow_steps = 30
        wait_seconds = 2
        orig_bg = self.original_background
        orig_rect = orig_bg.get_rect()
        target_rect = orig_rect.copy()
        # Start from the cropped background
        start_rect = self.background.get_rect(topleft=self.origin)
        for step in range(1, grow_steps + 1):
            lerp = step / grow_steps

            # Interpolate rect
            new_width = int(
                start_rect.width + (target_rect.width - start_rect.width) * lerp
            )
            new_height = int(
                start_rect.height + (target_rect.height - start_rect.height) * lerp
            )

            # Scale and blit
            scaled_bg = pg.transform.smoothscale(orig_bg, (new_width, new_height))
            rect = scaled_bg.get_rect(
                center=(self.screen.get_rect().centerx, scaled_bg.get_height() // 2)
            )
            self.screen.fill((0, 0, 0))
            self.starfield.update()
            self.starfield.draw(self.screen)
            self.screen.blit(scaled_bg, rect)

            pg.display.flip()
            self.clock.tick(60)
        # Wait a few seconds
        start_time = time.time()
        fade = sprite.ScreenFade()

        while time.time() - start_time < wait_seconds or fade.is_ascending():
            self.screen.fill((0, 0, 0))
            self.starfield.update()
            self.starfield.draw(self.screen)
            fade.update()

            self.screen.blit(
                orig_bg,
                orig_bg.get_rect(
                    center=(self.screen.get_rect().centerx, orig_bg.get_height() // 2)
                ),
            )
            fade.draw(self.screen)
            pg.display.flip()
            self.clock.tick(60)

            if time.time() - start_time >= wait_seconds and not fade.playing:
                fade.start(0.012)


if __name__ == "__main__":
    import pygame as pg

    pg.init()
    display = pg.display.set_mode(
        (1920, 1080), flags=pg.SCALED, vsync=1
    )  # scaled to fix screen tearing (found on reddit)
    from puzzlepiece import PuzzlePiece
    from puzzlemanager import PuzzleManager
    from player import Player
    from levelconfig import LEVELS, LevelConfig
    import sprite
    import time

    game = Game(display)
    game.run()
