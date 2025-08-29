import minigame
import pygame as pg

import globalSurfaces as gs


class LevelConfig:
    def __init__(self, minigames: list, background: pg.Surface):
        self.minigames = minigames
        self.background = background


# level 1
LEVEL_1 = LevelConfig(
    minigames=[
        minigame.Quiz("Choup !", ["Choup !", "Kipik."], question="Choupchoup ?"),
        minigame.Memory((4, 4), gs.MEMORY_CARDS_1),
        minigame.Quiz(
            "Rășinari",
            ["Rășinari", "Poplaca", "Păltiniș"],
            caption_image=gs.RASINARI_PHOTO,
            question="Où a été prise cette photo ?",
        ),
        minigame.ColorSequenceMemory(5),
    ],
    background=gs.LEVELS_SPRITES[0],
)

LEVEL_2 = LevelConfig(
    minigames=[
        minigame.ColorSequenceMemory(8),
        minigame.Quiz("Answer 9", ["Answer 9", "Answer 10"]),
        minigame.Quiz("Answer 11", ["Answer 11", "Answer 12"]),
        minigame.Quiz("Answer 13", ["Answer 13", "Answer 14"]),
    ],
    background=gs.LEVELS_SPRITES[1],
)

LEVEL_3 = LevelConfig(
    minigames=[
        minigame.Quiz(
            "2011",
            ["2011", "2013", "2016"],
            caption_image=gs.PHOTO_OF_2011,
            question="Quand a été prise cette photo ?",
        ),
        minigame.ColorSequenceMemory(13),
        minigame.Quiz(
            "Louane", ["Louane", "Isabelle"], question="Qui n'aime pas les poireaux?"
        ),
        minigame.SlidingPuzzle((3, 3), gs.LEVELS_SPRITES[0]),
    ],
    background=gs.LEVELS_SPRITES[2],
)

LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]
