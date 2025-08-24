import sprite

# this file is used to store global surfaces that are used in multiple files


LEVELS_SPRITES = [sprite.load_image("assets/images/placeholderFamille.png", size=(1100, 1100))]

PUZZLE_PIECE = sprite.load_image("assets/images/puzzlepiece.png", 1.1)
BUTTON_UP = sprite.load_image("assets/images/buttonUp.png", 0.5)
BUTTON_DOWN = sprite.load_image("assets/images/buttonDown.png", 0.5)


PLAYER_SPRITESHEET = sprite.Spritesheet(sprite.load_image("assets/images/spritesheetMC.png", 0.2), (int(500 / 5), int(1080 / 5)))
PLAYER_ANIMATION = sprite.Animation(PLAYER_SPRITESHEET, 0, 4, speed=10, repeat=True)

