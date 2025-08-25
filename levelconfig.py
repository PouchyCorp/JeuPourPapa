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
        minigame.Quiz("Answer 1", ["Answer 1", "Answer 2"], 0),
        minigame.Memory(["assets/images/mem1.png", "assets/images/mem2.png", "assets/images/mem3.png", "assets/images/mem4.png"]),
        minigame.Quiz("Answer 5", ["Answer 5", "Answer 6"], 0),
        minigame.Quiz("Answer 7", ["Answer 7", "Answer 8"], 0)
    ]
    , background = gs.LEVELS_SPRITES[0]
)

LEVEL_2 = LevelConfig(
    minigames = [
        minigame.Quiz("Answer 9", ["Answer 9", "Answer 10"], 0),
        minigame.Quiz("Answer 11", ["Answer 11", "Answer 12"], 0),
        minigame.Quiz("Answer 13", ["Answer 13", "Answer 14"], 0),
        minigame.Quiz("Answer 15", ["Answer 15", "Answer 16"], 0)
    ]
    , background = gs.LEVELS_SPRITES[0]
)

LEVELS = [LEVEL_1, LEVEL_2]