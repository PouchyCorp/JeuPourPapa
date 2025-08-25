import pygame as pg
from puzzlepiece import PuzzlePiece


class PuzzleManager:
    def __init__(self, boundaries : list[pg.Rect], puzzle_pieces : list[(PuzzlePiece, pg.Rect)], minigames : dict):
        assert len(puzzle_pieces) == 4, "There must be exactly 4 puzzle pieces"
        self.minigames_puzzlepiece_epic_duo : list[(PuzzlePiece, any)] = []  # Dictionary to store minigames linked to puzzle pieces
        self.link_minigames_to_pieces(boundaries, minigames, puzzle_pieces)

    def link_minigames_to_pieces(self, boundaries : list[pg.Rect], minigames : dict, puzzle_pieces : list[(PuzzlePiece, pg.Rect)]):
        """Link each puzzle piece to a minigame from the provided dictionary."""
        for i, (piece, refc) in enumerate(puzzle_pieces):
            if i < len(minigames):
                minigames[i].boundary = boundaries[i]
                self.minigames_puzzlepiece_epic_duo.append((piece, minigames[i]))
            else:
                self.minigames_puzzlepiece_epic_duo.append((piece, None))

    def update(self):
        """Update the active minigame."""
        for piece, minigame in self.minigames_puzzlepiece_epic_duo:
            if minigame and minigame.completed and not piece.playing_fade_animation and not piece.collected:
                piece.collect()
            elif minigame:
                minigame.update()

    def handle_event(self, event):
        """Handle events for the puzzle manager and active minigame."""
        for piece, minigame in self.minigames_puzzlepiece_epic_duo:
            if minigame and not piece.collected and not piece.playing_fade_animation and not minigame.completed:
                minigame.handle_event(event)
        
    def draw(self, surface : pg.Surface):
        # Draw puzzle pieces
        for piece, _ in self.minigames_puzzlepiece_epic_duo:
            piece.draw(surface)
        
        for _, minigame in self.minigames_puzzlepiece_epic_duo: # Iterate twice to draw pieces below minigame
            if minigame and not piece.collected and not minigame.completed:
                minigame.draw(surface)

    
    def is_all_pieces_collected(self) -> bool:
        """Check if all puzzle pieces have been collected."""
        return all(piece.collected for piece, _ in self.minigames_puzzlepiece_epic_duo)