class Game:
    def __init__(self, display):
        pg.init()
        self.screen : pg.Surface = display
        pg.display.set_caption("TOP SECRET")
        self.clock = pg.time.Clock()
        self.player = Player(400, 300)
        self.level = 0
        self.running = True
        self.origin = (410, 0)
        
        # Initialize starfield background
        from starfield import Starfield
        self.starfield = Starfield(self.screen.get_width(), self.screen.get_height(), num_stars=120)
    
    def init_level(self, level_ind : int):
        self.background = LEVELS[level_ind].background
        side_without_bitoniau = 550
        bitoniau = 88
        piece_size = (side_without_bitoniau, side_without_bitoniau)
        self.puzzle_pieces = [
            (PuzzlePiece(*self.origin, [162,112,112], rotation=0), pg.Rect(self.origin, piece_size)),
            (PuzzlePiece(self.origin[0] + side_without_bitoniau, self.origin[1], [171,148,124], rotation=270), pg.Rect((self.origin[0] + side_without_bitoniau, self.origin[1]), piece_size)),
            (PuzzlePiece(self.origin[0], self.origin[1] + side_without_bitoniau - bitoniau, [155,179,147], rotation=90), pg.Rect((self.origin[0], self.origin[1] + side_without_bitoniau), piece_size)),
            (PuzzlePiece(self.origin[0] + side_without_bitoniau - bitoniau, self.origin[1] + side_without_bitoniau, [160,185,190], rotation=180), pg.Rect((self.origin[0] + side_without_bitoniau, self.origin[1] + side_without_bitoniau), piece_size))
        ]

        boundaries = []
        for i in range(4):
            boundaries.append(pg.Rect((self.origin[0] + side_without_bitoniau * (i % 2), self.origin[1] + side_without_bitoniau * (i // 2)),
                                       (side_without_bitoniau, side_without_bitoniau)))

        self.puzzle_manager = PuzzleManager(boundaries, self.puzzle_pieces, LEVELS[level_ind].minigames)

    def run(self):
        while self.level < len(LEVELS) and self.running:
            self.finished_level = False
            self.init_level(self.level)
            while not self.finished_level and self.running:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)
            self.level += 1
        pg.quit()

    def handle_events(self):
        self.player.handle_movement_inputs()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            self.puzzle_manager.handle_event(event)
            
            self.player.handle_events(event)
            
            

    def update(self):
        self.player.update()
        self.puzzle_manager.update()
        if self.puzzle_manager.is_all_pieces_collected():
            self.finished_level = True
        self.starfield.update()  # Update starfield animation

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
        
        pg.display.flip()

if __name__ == "__main__":
    import pygame as pg
    pg.init()
    display = pg.display.set_mode((1920, 1080), flags=pg.SCALED, vsync=1) # scaled to fix screen tearing (found on reddit)
    from puzzlepiece import PuzzlePiece
    from puzzlemanager import PuzzleManager
    from player import Player
    from levelconfig import LEVELS, LevelConfig
    game = Game(display)
    game.run()