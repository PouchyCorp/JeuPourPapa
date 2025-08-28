import minigame
import pygame as pg

import globalSurfaces as gs

class LevelConfig:
    def __init__(self, minigames : list, background: pg.Surface):
        self.minigames = minigames
        self.background = background

# level 1
LEVEL_1 = LevelConfig(
    minigames = [
        minigame.Quiz("Answer 1", ["Answer 1", "Answer 2"], caption_image=gs.PUZZLE_PIECE),
        minigame.Memory((4, 4), gs.MEMORY_CARDS_1),
        minigame.SlidingPuzzle((3, 3), gs.LEVELS_SPRITES[0]),
        minigame.ColorSequenceMemory(5)
    ]
    , background = gs.LEVELS_SPRITES[0]
)

LEVEL_2 = LevelConfig(
    minigames = [
        minigame.Quiz("Answer 9", ["Answer 9", "Answer 10"]),
        minigame.Quiz("Answer 11", ["Answer 11", "Answer 12"]),
        minigame.Quiz("Answer 13", ["Answer 13", "Answer 14"]),
        minigame.Quiz("Answer 15", ["Answer 15", "Answer 16"])
    ]
    , background = gs.LEVELS_SPRITES[0]
)

LEVELS = [LEVEL_1, LEVEL_2]