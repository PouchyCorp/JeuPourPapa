import sprite

# this file is used to store global surfaces that are used in multiple files

FAMILY_PLACEHOLDER = sprite.load_image("assets/images/placeholderFamille.png")

PLAYER_SPRITESHEET = sprite.Spritesheet(sprite.load_image("assets/images/spritesheetMC.png", 0.2), (int(500 / 5), int(1080 / 5)))
PLAYER_ANIMATION = sprite.Animation(PLAYER_SPRITESHEET, 0, 4, speed=10, repeat=True)