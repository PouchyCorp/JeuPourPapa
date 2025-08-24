import pygame as pg
from globalSurfaces import BUTTON_UP, BUTTON_DOWN
from puzzlepiece import PuzzlePiece
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from minigame import MinigameBase


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

    def draw(self, surface : pg.Surface):
        surface.blit(self.surf, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        if event.type == pg.USEREVENT + 0 and self.rect.collidepoint(event.pos):
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


class PuzzleManager:
    def __init__(self, boundary : pg.Rect, puzzle_pieces : list[(PuzzlePiece, pg.Rect)], minigames : dict):
        assert len(puzzle_pieces) == 4, "There must be exactly 4 puzzle pieces"
        self.minigames_puzzlepiece_epic_duo : list[(PuzzlePiece, any)] = []  # Dictionary to store minigames linked to puzzle pieces
        self.link_minigames_to_pieces(boundary, minigames, puzzle_pieces)
        
    def link_minigames_to_pieces(self, boundary, minigames : dict, puzzle_pieces : list[(PuzzlePiece, pg.Rect)]):
        """Link each puzzle piece to a minigame from the provided dictionary."""
        for i, (piece, refc) in enumerate(puzzle_pieces):
            if i < len(minigames):
                minigames[i].boundary = boundary
                self.minigames_puzzlepiece_epic_duo.append((piece, minigames[i]))
            else:
                self.minigames_puzzlepiece_epic_duo.append((piece, None))

    def update(self):
        """Update the active minigame."""
        for piece, minigame in self.minigames_puzzlepiece_epic_duo:
            if minigame and minigame.completed and not piece.collected:
                piece.collect()
            elif minigame:
                minigame.update()

    def handle_event(self, event):
        """Handle events for the puzzle manager and active minigame."""
        for piece, minigame in self.minigames_puzzlepiece_epic_duo:
            if minigame and not piece.collected and not minigame.completed:
                minigame.handle_event(event)
        
    def draw(self, surface : pg.Surface):
        # Draw puzzle pieces
        for piece, minigame in self.minigames_puzzlepiece_epic_duo:
            piece.draw(surface)
            if minigame and not piece.collected and not minigame.completed:
                minigame.draw(surface)

    
    def is_all_pieces_collected(self) -> bool:
        """Check if all puzzle pieces have been collected."""
        return all(piece.collected for piece, _ in self.minigames_puzzlepiece_epic_duo)