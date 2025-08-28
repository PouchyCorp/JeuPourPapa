import pygame


class keyboard_class:
    def __init__(self):
        self.pressed_keys = []
        self.mouse_position = pygame.Vector2(pygame.mouse.get_pos())

        self.click_map = {
            0: "left click",
            1: "right click",
            2: "middle click",
            3: "fourth click",  # the button on the side that's near the hand (fourth button)
            4: "fifth click",  # the button on the side that's far to the hand (fifth button)
        }

    def key_press(self, key):
        self.pressed_keys.append(pygame.key.name(key))

    def key_release(self, key):
        self.pressed_keys.remove(pygame.key.name(key))

    def step(self):

        self.mouse_position = pygame.Vector2(pygame.mouse.get_pos())

        clicks_pressed = pygame.mouse.get_pressed(5)

        for click_checked in range(5):
            if clicks_pressed[click_checked]:
                if self.click_map[click_checked] not in self.pressed_keys:
                    self.pressed_keys.append(self.click_map[click_checked])
            elif self.click_map[click_checked] in self.pressed_keys:
                self.pressed_keys.remove(self.click_map[click_checked])


keyboard = keyboard_class()
