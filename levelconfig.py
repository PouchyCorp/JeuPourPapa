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
        minigame.ColorSequenceMemory(7),
    ],
    background=gs.LEVELS_SPRITES[0],
)

LEVEL_2 = LevelConfig(
    minigames=[
        minigame.ColorSequenceMemory(12),
        minigame.Quiz(
            "Ouais <3",
            ["Ouais <3", "Trop ringard ..."],
            "Est-il bien sapé ?",
            gs.PAPA_PERRUQUE,
        ),  # papa perruque
        minigame.Quiz(
            "Louis", ["Paul", "Philippe", "Louis"], "Qui est-ce ?", gs.LOUIS_PHOTO
        ),
        minigame.Quiz(
            "Beaufort",
            ["Emmental", "Beaufort", "Gruyère"],
            "Quel est ce fromage ?",
            gs.CHEESE_PHOTO,
        ),
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
            "Marius",
            ["Marius", "Mark", "Sam"],
            question="Le bus de ..?",
            caption_image=gs.HISOITRE_PHOTO,
        ),
        minigame.SlidingPuzzle((3, 3), gs.LEVELS_SPRITES[0]),
    ],
    background=gs.LEVELS_SPRITES[2],
)

LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]
