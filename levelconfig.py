from minigame import GenericQuiz
import pygame as pg
from puzzlepiece import PuzzlePiece
from puzzlemanager import PuzzleManager

import globalSurfaces as gs

class LevelConfig:
    def __init__(self, minigames : list, background: pg.Surface):
        self.minigames = minigames
        self.background = background


# level 1
LEVEL_1 = LevelConfig(
    minigames = [
        GenericQuiz("Answer 1", ["Answer 1", "Answer 2"], 0),
        GenericQuiz("Answer 3", ["Answer 3", "Answer 4"], 0),
        GenericQuiz("Answer 5", ["Answer 5", "Answer 6"], 0),
        GenericQuiz("Answer 7", ["Answer 7", "Answer 8"], 0)
    ]
    , background = gs.LEVELS_SPRITES[0]
)

LEVEL_2 = LevelConfig(
    minigames = [
        GenericQuiz("Answer 9", ["Answer 9", "Answer 10"], 0),
        GenericQuiz("Answer 11", ["Answer 11", "Answer 12"], 0),
        GenericQuiz("Answer 13", ["Answer 13", "Answer 14"], 0),
        GenericQuiz("Answer 15", ["Answer 15", "Answer 16"], 0)
    ]
    , background = gs.LEVELS_SPRITES[0]
)

LEVELS = [LEVEL_1, LEVEL_2]