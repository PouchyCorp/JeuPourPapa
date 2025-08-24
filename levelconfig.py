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
        GenericQuiz("Answer 1", ["Answer 1", "Answer 2"], 0),
        GenericQuiz("Answer 1", ["Answer 1", "Answer 2"], 0),
        GenericQuiz("Answer 1", ["Answer 1", "Answer 2"], 0)
    ]
    , background = gs.LEVELS_SPRITES[0]
)


LEVELS = [LEVEL_1]