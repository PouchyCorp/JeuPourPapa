import pygame as pg


def run(clock: pg.time.Clock, display: pg.Surface):

    ## paul si tu passes par là, ne touches rien, t'inquiète, ça marche uwu

    global walpaper
    walpaper = pg.image.load(
        "assets\start_assets\wallpaper.jpg"
    )  # image has to be 1920/1080, it doesn't get resized

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

    is_fading = False
    fade_number = 0
    fade_increment = 40

    def apply_black_fade(fade_number: int = fade_number):
        fade_color = pg.Color(fade_number, fade_number, fade_number)
        fade_screeen = pg.Surface(display.get_size())
        fade_screeen.fill(fade_color)
        display.blit(fade_screeen, (0, 0), special_flags=pg.BLEND_RGBA_SUB)

    running = True

    while running:

        display.blit(walpaper, (0, 0))

        show_happy_birthday(200, 50)
        show_press_key(900, 40)

        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYUP:
                running = False

        if is_fading:
            fade_number += fade_increment

        apply_black_fade(255)
        pg.display.flip()
        display.fill("black")
        clock.tick_busy_loop(60)
