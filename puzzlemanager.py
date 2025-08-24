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
    
    def reset(self):
        self.state = 'UP'
        self.surf = BUTTON_UP


class PuzzleManager:
    def __init__(self, puzzle_pieces : list[(PuzzlePiece, pg.Rect)]):
        assert len(puzzle_pieces) == 4, "There must be exactly 4 puzzle pieces"
        self.puzzle_pieces = puzzle_pieces
        self.minigames = {}  # Dictionary to store minigames linked to puzzle pieces
        self.active_minigame: Optional['MinigameBase'] = None
        
    def add_minigame(self, puzzle_piece: PuzzlePiece, minigame: 'MinigameBase'):
        """Add a minigame linked to a specific puzzle piece."""
        self.minigames[id(puzzle_piece)] = minigame
    
    def start_minigame(self, puzzle_piece: PuzzlePiece):
        """Start the minigame associated with the given puzzle piece."""
        piece_id = id(puzzle_piece)
        if piece_id in self.minigames:
            if self.active_minigame:
                self.active_minigame.deactivate()
            
            self.active_minigame = self.minigames[piece_id]
            self.active_minigame.activate()
            return True
        return False
    
    def check_puzzle_piece_interaction(self, event):
        """Check if a puzzle piece was interacted with and start its minigame."""
        if event.type == pg.USEREVENT + 0:  # Player action event
            player_pos = event.pos
            for piece, interaction_rect in self.puzzle_pieces:
                if not piece.collected and interaction_rect.collidepoint(player_pos):
                    if self.start_minigame(piece):
                        return True
        return False
    
    def update(self):
        """Update the active minigame."""
        if self.active_minigame and self.active_minigame.is_active:
            self.active_minigame.update()
            
            # Check if minigame was completed
            if self.active_minigame.is_completed:
                self.active_minigame = None

    def handle_event(self, event):
        """Handle events for the puzzle manager and active minigame."""
        # First check if a puzzle piece was interacted with
        if not self.active_minigame and self.check_puzzle_piece_interaction(event):
            return True
        
        # If there's an active minigame, let it handle the event
        if self.active_minigame and self.active_minigame.is_active:
            self.active_minigame.handle_event(event)
            return True
        
        return False

    def draw(self, surface : pg.Surface):
        # Draw puzzle pieces
        for piece, _ in self.puzzle_pieces:
            piece.draw(surface)
        
        # Draw active minigame
        if self.active_minigame and self.active_minigame.is_active:
            self.draw_minigame_overlay(surface)
            self.active_minigame.draw(surface)
    
    def draw_minigame_overlay(self, surface: pg.Surface):
        """Draw a semi-transparent overlay when a minigame is active."""
        overlay = pg.Surface(surface.get_size())
        overlay.set_alpha(128)  # Semi-transparent
        overlay.fill((0, 0, 0))  # Black overlay
        surface.blit(overlay, (0, 0))
        
        # Draw minigame title
        if self.active_minigame:
            font = pg.font.SysFont("Arial", 48)
            title_surf = font.render(self.active_minigame.name, True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(surface.get_width() // 2, 50))
            surface.blit(title_surf, title_rect)
    
    def is_all_pieces_collected(self) -> bool:
        """Check if all puzzle pieces have been collected."""
        return all(piece.collected for piece, _ in self.puzzle_pieces)
    
    def get_collected_count(self) -> int:
        """Get the number of collected puzzle pieces."""
        return sum(1 for piece, _ in self.puzzle_pieces if piece.collected)