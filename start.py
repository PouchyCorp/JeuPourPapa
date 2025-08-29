import pygame as pg

import sprite
from globalSurfaces import START_GAME_SOUND, WALLPAPER_START


def run(clock: pg.time.Clock, display: pg.Surface):

    ## paul si tu passes par là, ne touches rien, t'inquiète, ça marche uwu

    pg.mixer.music.play(-1)

    def show_happy_birthday(y: int, size: float):
        fun_font = pg.font.Font("assets\start_assets\\fun font.ttf", size)

        happy_birthday = fun_font.render("Joyeux Anniversaires, Papa!", True, "pink")

        image_rect = happy_birthday.get_rect(center=(display.get_width() / 2, y))

        display.blit(happy_birthday, image_rect)

    def show_press_key(y: int, size: float):
        text_font = pg.font.Font("assets\start_assets\\under_text_font.ttf", size)

        happy_birthday = text_font.render("Press any key to start", True, "black")

        image_rect = happy_birthday.get_rect(center=(display.get_width() / 2, y))

        display.blit(happy_birthday, image_rect)

    running = True
    fade = sprite.ScreenFade()
    while running or fade.is_ascending():
        display.blit(WALLPAPER_START, (0, 0))

        show_happy_birthday(200, 50)
        show_press_key(900, 40)

        fade.draw(display)
        fade.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                from sys import exit

                exit()
            if event.type == pg.KEYUP and running:
                START_GAME_SOUND.play()
                fade.start(0.012)
                running = False

        pg.display.flip()
        display.fill("black")
        clock.tick_busy_loop(60)
