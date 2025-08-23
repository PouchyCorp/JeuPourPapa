import pygame as pg

class Game:
    def __init__(self, display):
        pg.init()
        self.screen = display
        pg.display.set_caption("TOP SECRET")
        self.clock = pg.time.Clock()
        self.player = Player(400, 300)
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pg.quit()

    def handle_events(self):
        self.player.handle_movement_inputs()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            
            self.player.handle_events(event)

    def update(self):
        self.player.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)

        # show fps
        fps = int(self.clock.get_fps())
        font = pg.font.SysFont("Arial", 30)
        fps_surf = font.render(f"FPS: {fps}", True, (255, 255, 255))
        self.screen.blit(fps_surf, (10, 10))
        pg.display.flip()


if __name__ == "__main__":
    pg.init()
    display = pg.display.set_mode((1920, 1080), flags=pg.SCALED, vsync=1) # scaled to fix screen tearing (found on reddit)

    from player import Player
    game = Game(display)
    game.run()