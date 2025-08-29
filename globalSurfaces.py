import sprite
import pygame as pg

# this file is used to store global surfaces that are used in multiple files


LEVELS_SPRITES = [
    sprite.load_image("assets/photos/4.png"),
    sprite.load_image("assets/photos/2.png"),
    sprite.load_image("assets/photos/6.png")
]

PUZZLE_PIECE = sprite.load_image("assets/images/puzzlepiece.png", 1.1)
BUTTON_UP = sprite.load_image("assets/images/buttonUp.png", 0.5)
BUTTON_DOWN = sprite.load_image("assets/images/buttonDown.png", 0.5)

MEMORY_CARDS_1 = [
    sprite.load_image(f"assets/mem images/mem{i}.jpg", 0.3) for i in range(1, 9)
]


PLAYER_SPRITESHEET = sprite.Spritesheet(
    sprite.load_image("assets/images/spritesheetMC.png", 0.2),
    (int(500 / 5), int(1080 / 5)),
)
PLAYER_ANIMATION = sprite.Animation(PLAYER_SPRITESHEET, 0, 4, speed=10, repeat=True)


RED_BUTTON_SOUND = pg.mixer.Sound("assets/sound/red.wav")
YELLOW_BUTTON_SOUND = pg.mixer.Sound("assets/sound/yellow.wav")
BLUE_BUTTON_SOUND = pg.mixer.Sound("assets/sound/blue.wav")
GREEN_BUTTON_SOUND = pg.mixer.Sound("assets/sound/green.wav")


BUTTON_PUSHED_SOUND = pg.mixer.Sound("assets/sound/button_pushed.wav")


ACHIEVE_LEVEL_SOUND = pg.mixer.Sound("assets/sound/achieve_level.mp3")
START_GAME_SOUND = pg.mixer.Sound("assets/sound/start_of_game_alt.mp3")
ACHIEVE_PUZZLE_SOUND = pg.mixer.Sound("assets/sound/achieve_puzzle.wav")
ERROR_MEMORY_SOUND = pg.mixer.Sound("assets/sound/error_memory.mp3")
