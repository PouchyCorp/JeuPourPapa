import pygame as pg
from puzzlepiece import PuzzlePiece
from time import time
import random


class GenericMinigame:
    def __init__(self, name="Minigame"):
        self.boundary = None  # Will be set by PuzzleManager
        self.completed = False
        self.name = name
        self.is_completed_countdown = None
        self.fade_alpha = 255
        self.minigame_screenshot = None

    def setup(self):
        pass  # To be implemented by subclasses if needed

    def update(self):
        if self.completed:
            return
        if self.is_completed_countdown and time() >= self.is_completed_countdown:
            self.completed = True

    def draw(self, surface: pg.Surface, screenshot_mode=False):
        if (
            self.is_completed_countdown
            and self.fade_alpha == 255
            and not screenshot_mode
        ):
            self.minigame_screenshot = pg.Surface(surface.get_size(), pg.SRCALPHA)
            self.draw(self.minigame_screenshot, screenshot_mode=True)
            self.fade_alpha -= 1

        if self.is_completed_countdown and self.fade_alpha > 0 and not screenshot_mode:
            self.fade_alpha -= 5
            self.minigame_screenshot.set_alpha(self.fade_alpha)
            surface.blit(self.minigame_screenshot, (0, 0))

            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.completed = True
            return
        elif self.completed and not screenshot_mode:
            return

    def handle_event(self, event: pg.event.Event):
        pass  # To be implemented by subclasses if needed


class Quiz(GenericMinigame):
    def __init__(
        self,
        right_answer,
        possible_answers,
        question: str = "Répond à la question !",
        caption_image=None,
    ):
        super().__init__(name="Quiz")
        self.question = question
        self.right_answer = right_answer
        self.possible_answers = possible_answers
        self.caption_image = caption_image
        self.buttons = []

    def setup(self):
        if not self.boundary:
            return
        from Button import Button
        from globalSurfaces import BUTTON_UP
        import random

        self.buttons: list[Button] = []
        num_answers = len(self.possible_answers)
        button_width = BUTTON_UP.get_width()
        button_height = BUTTON_UP.get_height()
        spacing = 60

        total_width = num_answers * button_width + (num_answers - 1) * spacing
        start_x = self.boundary.centerx - total_width // 2
        y = self.boundary.bottom - button_height - 40

        for i, answer in enumerate(self.possible_answers):
            rect = pg.Rect(
                start_x + i * (button_width + spacing), y, button_width, button_height
            )
            button = Button(rect, answer, (255, 255, 255), 30)
            self.buttons.append(button)

    def update(self):
        super().update()
        if self.completed:
            return

        if not self.buttons and self.boundary:
            self.setup()

        for button in self.buttons:
            if button.state == "DOWN" and button.text == self.right_answer:
                self.is_completed_countdown = time() + 1

        for button in self.buttons:
            if (
                button.state == "DOWN"
                and button.last_pressed_time
                and time() - button.last_pressed_time >= 1
            ):
                button.reset()
                break

    def draw(self, surface: pg.Surface, screenshot_mode=False):
        super().draw(surface, screenshot_mode)
        if self.completed and not screenshot_mode:
            return

        if self.caption_image:
            img_w, img_h = self.caption_image.get_size()
            max_w = self.boundary.width - 100
            max_h = self.boundary.height // 3
            scale = min(max_w / img_w, max_h / img_h, 1)
            new_size = (int(img_w * scale), int(img_h * scale))
            img = pg.transform.smoothscale(self.caption_image, new_size)
            img_rect = img.get_rect(
                center=(self.boundary.centerx, self.boundary.centery - 50)
            )
            surface.blit(img, img_rect)

        font = pg.font.SysFont("Arial", 48)
        question_surf = font.render(self.question, True, (255, 255, 255))
        question_rect = question_surf.get_rect(
            center=(self.boundary.centerx, self.boundary.top + 50)
        )
        surface.blit(question_surf, question_rect)

        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event: pg.event.Event):
        if self.completed:
            return
        for button in self.buttons:
            button.handle_event(event)


class Memory(GenericMinigame):
    def __init__(self, grid_size=(4, 4), images=None):
        super().__init__(name="MemoryGame")
        self.grid_size = grid_size
        self.images = images or []
        self.cards = []
        self.flipped = []
        self.matched = set()
        self.card_size = (110, 110)
        self.last_flip_time = None
        self.setup()
        from globalSurfaces import (
            BUTTON_PUSHED_SOUND,
            WIN_MEMORY_SOUND,
            ERROR_MEMORY_SOUND,
        )

        self.sound = BUTTON_PUSHED_SOUND
        self.error_sound = ERROR_MEMORY_SOUND
        self.win_sound = WIN_MEMORY_SOUND

    def setup(self):
        if not self.boundary:
            return

        num_cards = self.grid_size[0] * self.grid_size[1]
        assert num_cards % 2 == 0, "Grid must have even number of cards"
        images = self.images * (num_cards // (2 * len(self.images)))
        images += random.sample(self.images, num_cards // 2 - len(images))
        images = images * 2

        # Create pairs of image indices instead of duplicating images
        image_pairs = list(range(len(images) // 2)) * 2
        random.shuffle(image_pairs)

        self.cards = []
        w, h = self.card_size
        spacing = 20
        total_w = self.grid_size[0] * w + (self.grid_size[0] - 1) * spacing
        total_h = self.grid_size[1] * h + (self.grid_size[1] - 1) * spacing
        start_x = self.boundary.centerx - total_w // 2
        start_y = self.boundary.centery - total_h // 2

        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                idx = y * self.grid_size[0] + x
                rect = pg.Rect(
                    start_x + x * (w + spacing), start_y + y * (h + spacing), w, h
                )

                image_idx = image_pairs[idx]
                original_image = images[image_idx]
                resized_image = pg.transform.scale(
                    original_image, (self.card_size[0] - 10, self.card_size[1] - 10)
                )

                self.cards.append(
                    {
                        "rect": rect,
                        "image": original_image,
                        "resized": resized_image,
                        "flipped": False,
                        "matched": False,
                        "index": idx,
                        "pair_id": image_idx,  # Add pair identifier for matching
                    }
                )

        print(f"Memory game setup with {len(self.cards)} cards.")

    def update(self):
        super().update()
        if self.completed:
            return

        if not self.cards:
            self.setup()

        if len(self.flipped) == 2 and not self.last_flip_time:
            self.last_flip_time = time()

        if self.last_flip_time and time() - self.last_flip_time > 1:
            idx1, idx2 = self.flipped
            if self.cards[idx1]["pair_id"] == self.cards[idx2]["pair_id"]:
                self.cards[idx1]["matched"] = True
                self.cards[idx2]["matched"] = True

                self.matched.add(idx1)
                self.matched.add(idx2)
                self.win_sound.play()
            else:
                self.error_sound.play()

            self.cards[idx1]["flipped"] = False
            self.cards[idx2]["flipped"] = False
            self.flipped = []
            self.last_flip_time = None

        if (
            all(card["matched"] for card in self.cards)
            and not self.completed
            and not self.is_completed_countdown
        ):
            print("Memory game completed!")
            self.is_completed_countdown = time() + 1

    def draw(self, surface: pg.Surface, screenshot_mode=False):
        super().draw(surface, screenshot_mode)
        if self.completed and not screenshot_mode:
            return

        font = pg.font.SysFont("Arial", 48)
        title_surf = font.render("Memory Game", True, (255, 255, 255))
        title_rect = title_surf.get_rect(
            center=(self.boundary.centerx, self.boundary.top + 60)
        )
        surface.blit(title_surf, title_rect)

        for card in self.cards:
            color = (
                (200, 200, 200) if card["flipped"] or card["matched"] else (50, 50, 50)
            )
            pg.draw.rect(surface, color, card["rect"])
            pg.draw.rect(surface, (255, 255, 255), card["rect"], 2)
            if card["flipped"] or card["matched"]:
                if isinstance(card["resized"], pg.Surface):
                    surface.blit(
                        card["resized"], (card["rect"].x + 5, card["rect"].y + 5)
                    )
                else:
                    img_font = pg.font.SysFont("Arial", 36)
                    img_surf = img_font.render(str(card["image"]), True, (0, 0, 0))
                    img_rect = img_surf.get_rect(center=card["rect"].center)
                    surface.blit(img_surf, img_rect)

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.USEREVENT + 0:
            pos = event.pos
            for idx, card in enumerate(self.cards):
                if (
                    card["rect"].collidepoint(pos)
                    and not card["flipped"]
                    and not card["matched"]
                    and self.last_flip_time is None
                ):
                    card["flipped"] = True
                    self.sound.play()

                    self.flipped.append(idx)
                    if len(self.flipped) > 2:
                        # Should not happen, but reset if it does
                        for i in self.flipped:
                            self.cards[i]["flipped"] = False
                        self.flipped = [idx]
                    break


class SlidingPuzzle(GenericMinigame):
    def __init__(self, grid_size=(4, 4), image: pg.Surface = None):
        super().__init__(name="SlidingPuzzle")
        self.grid_size = grid_size
        self.tiles = []
        self.empty_pos = (grid_size[0] - 1, grid_size[1] - 1)
        self.tile_size = (100, 100)
        self.image = image
        self.shuffling = True
        self.setup_done = False
        self.moved_indexes = None

        from globalSurfaces import BUTTON_PUSHED_SOUND

        self.sound = BUTTON_PUSHED_SOUND

    def setup(self):
        if not self.boundary:
            return
        w, h = (
            self.boundary.width // self.grid_size[0],
            self.boundary.height // self.grid_size[1],
        )
        self.tile_size = (w, h)
        self.tiles = []
        self.image = pg.transform.scale(
            self.image,
            (
                self.grid_size[0] * self.tile_size[0],
                self.grid_size[1] * self.tile_size[1],
            ),
        )

        img = self.image
        if img is None:
            img = pg.Surface((w * self.grid_size[0], h * self.grid_size[1]))
            img.fill((150, 100, 200))
        for y in range(self.grid_size[1]):
            row = []
            for x in range(self.grid_size[0]):
                if (x, y) == (self.grid_size[0] - 1, self.grid_size[1] - 1):
                    row.append(None)
                else:
                    rect = pg.Rect(x * w, y * h, w, h)

                    tile_img = img.subsurface(rect).copy()
                    row.append({"img": tile_img, "pos": (x, y), "correct": (x, y)})
            self.tiles.append(row)
        self.empty_pos = (self.grid_size[0] - 1, self.grid_size[1] - 1)
        self.shuffle()
        self.setup_done = True

    def shuffle(self):
        # Perform a number of random valid moves to shuffle the puzzle
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        last_move = None
        for _ in range(100):
            x, y = self.empty_pos
            random.shuffle(moves)
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size[0] and 0 <= ny < self.grid_size[1]:
                    if last_move and (nx, ny) == last_move:
                        continue
                    self.tiles[y][x], self.tiles[ny][nx] = (
                        self.tiles[ny][nx],
                        self.tiles[y][x],
                    )
                    self.empty_pos = (nx, ny)
                    last_move = (x, y)
                    break

    def update(self):
        super().update()
        if self.completed:
            return
        if not self.setup_done and self.boundary:
            self.setup()
        # Check for completion
        solved = True
        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                tile = self.tiles[y][x]
                if tile is None:
                    continue
                if tile["correct"] != (x, y):
                    solved = False
        if solved and not self.is_completed_countdown:
            self.is_completed_countdown = time() + 1

        if self.moved_indexes:
            (y1, x1), (y2, x2) = self.moved_indexes
            if self.moved_lerp_increment > 0:
                self.moved_lerp_increment -= 1
            else:
                self.tiles[y1][x1], self.tiles[y2][x2] = (
                    self.tiles[y2][x2],
                    self.tiles[y1][x1],
                )
                self.empty_pos = (x1, y1)
                self.moved_indexes = None

    def draw(self, surface: pg.Surface, screenshot_mode=False):
        super().draw(surface, screenshot_mode)
        if self.completed and not screenshot_mode:
            return

        w, h = self.tile_size
        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                tile = self.tiles[y][x]
                if self.moved_indexes:
                    (my1, mx1), (my2, mx2) = self.moved_indexes
                    if (y, x) == (my1, mx1):
                        lerp = (10 - self.moved_lerp_increment) / 10
                        draw_x = self.boundary.left + (mx1 + (mx2 - mx1) * lerp) * w
                        draw_y = self.boundary.top + (my1 + (my2 - my1) * lerp) * h
                        rect = pg.Rect(draw_x, draw_y, w, h)
                    elif (y, x) == (my2, mx2):  # do nothing for the other tile
                        continue
                    else:
                        rect = pg.Rect(
                            self.boundary.left + x * w, self.boundary.top + y * h, w, h
                        )
                else:
                    rect = pg.Rect(
                        self.boundary.left + x * w, self.boundary.top + y * h, w, h
                    )
                if tile is None:
                    continue
                surface.blit(tile["img"], rect)
                pg.draw.rect(surface, (255, 255, 255), rect, 2)

    def handle_event(self, event: pg.event.Event):
        if self.completed:
            return
        if event.type == pg.USEREVENT + 0 and not self.moved_indexes:

            mx, my = event.pos
            width, height = self.tile_size
            grid_x = (mx - self.boundary.left) // width  # Grid x
            grid_y = (my - self.boundary.top) // height  # Grid y
            if 0 <= grid_x < self.grid_size[0] and 0 <= grid_y < self.grid_size[1]:
                empty_x, empty_y = self.empty_pos
                if (abs(grid_x - empty_x) == 1 and grid_y == empty_y) or (
                    abs(grid_y - empty_y) == 1 and grid_x == empty_x
                ):  # Check if adjacent
                    # Swap tile with empty
                    self.sound.play()
                    self.moved_indexes = ((grid_y, grid_x), (empty_y, empty_x))
                    self.moved_lerp_increment = 10


class ColorButton:
    def __init__(self, center, radius, color, flash_color, index):
        self.center = center
        self.radius = radius
        self.color = color
        self.flash_color = flash_color
        self.index = index
        self.flashing = False
        self.flash_end_time = 0
        from globalSurfaces import (
            GREEN_BUTTON_SOUND,
            RED_BUTTON_SOUND,
            YELLOW_BUTTON_SOUND,
            BLUE_BUTTON_SOUND,
        )

        COLOR_MAP = {  # je sais c'est moche mais du coup ça rend le code moins moche
            (100, 20, 20): RED_BUTTON_SOUND,
            (220, 40, 40): RED_BUTTON_SOUND,
            (20, 100, 20): GREEN_BUTTON_SOUND,
            (40, 220, 40): GREEN_BUTTON_SOUND,
            (20, 20, 100): BLUE_BUTTON_SOUND,
            (40, 40, 220): BLUE_BUTTON_SOUND,
            (100, 100, 20): YELLOW_BUTTON_SOUND,
            (220, 220, 40): YELLOW_BUTTON_SOUND,
        }
        self.sound_at_flash = COLOR_MAP[self.color]

    def draw(self, surface):
        draw_color = self.flash_color if self.flashing else self.color
        pg.draw.circle(surface, draw_color, self.center, self.radius)
        pg.draw.circle(surface, (255, 255, 255), self.center, self.radius, 4)

    def handle_event(self, event):
        if event.type == pg.USEREVENT + 0 and not self.flashing:
            if (
                pg.Vector2(event.pos) - pg.Vector2(self.center)
            ).length() <= self.radius:

                return True

        return False

    def flash(self, duration=0.4):
        self.sound_at_flash.play()

        self.flashing = True
        self.flash_end_time = time() + duration

    def update(self):
        if self.flashing and time() >= self.flash_end_time:
            self.flashing = False


class ColorSequenceMemory(GenericMinigame):
    COLORS = [
        ((100, 20, 20), (220, 40, 40)),  # Red
        ((20, 100, 20), (40, 220, 40)),  # Green
        ((20, 20, 100), (40, 40, 220)),  # Blue
        ((100, 100, 20), (220, 220, 40)),  # Yellow
    ]

    def __init__(self, sequence_length=4):
        super().__init__(name="ColorSequenceMemory")
        self.sequence_length = sequence_length
        self.sequence = []
        self.user_input = []
        self.buttons = []
        self.state = "waiting"  # waiting, showing, input, finished : FSM
        self.show_index = 0
        self.show_next_time = 0
        self.start_button = None
        self.message = "Memorise la séquence !"
        self.last_flash_time = 0

    def setup(self):
        if not self.boundary:
            return

        cx, cy = self.boundary.centerx, self.boundary.centery
        r = min(self.boundary.width, self.boundary.height) // 6
        offset = r * 2
        positions = [
            (cx - offset, cy - offset),
            (cx + offset, cy - offset),
            (cx - offset, cy + offset),
            (cx + offset, cy + offset),
        ]
        self.buttons = []
        for i, ((color, flash_color), pos) in enumerate(zip(self.COLORS, positions)):
            self.buttons.append(ColorButton(pos, r, color, flash_color, i))

        from Button import Button
        from globalSurfaces import BUTTON_UP

        button_width = BUTTON_UP.get_width()
        button_height = BUTTON_UP.get_height()
        rect = pg.Rect(
            cx - button_width // 2,
            self.boundary.bottom - 120,
            button_width,
            button_height,
        )
        self.start_button = Button(rect, "Commencer", (255, 255, 255))
        self.state = "waiting"
        self.sequence = []
        self.user_input = []
        self.show_index = 0

    def start_sequence(self, seq_length=4):
        self.sequence = [random.randint(0, 3) for _ in range(seq_length)]
        self.user_input = []
        self.state = "showing"
        self.show_index = 0
        self.show_next_time = time() + 0.5

    def update(self):
        super().update()
        if self.completed:
            return
        if not self.buttons and self.boundary:
            self.setup()
        for btn in self.buttons:
            btn.update()
        if self.state == "showing":
            now = time()
            if self.show_index < len(self.sequence):
                if now >= self.show_next_time:
                    idx = self.sequence[self.show_index]
                    self.buttons[idx].flash()
                    self.show_index += 1
                    self.show_next_time = now + 0.7
            else:
                # Wait for last flash to finish
                if all(not btn.flashing for btn in self.buttons):
                    self.state = "input"
                    self.message = "Reproduis la séquence !"

        elif self.state == "finished":
            if not self.is_completed_countdown:
                self.is_completed_countdown = time() + 1

    def draw(self, surface: pg.Surface, screenshot_mode=False):
        super().draw(surface, screenshot_mode)
        if self.completed and not screenshot_mode:
            return

        for btn in self.buttons:
            btn.draw(surface)
        # Draw start button
        if self.state == "waiting" and self.start_button:
            self.start_button.draw(surface)
        # Draw message
        if self.message:
            msg_font = pg.font.SysFont("Arial", 32)
            msg_surf = msg_font.render(self.message, True, (255, 255, 255))
            msg_rect = msg_surf.get_rect(
                center=(self.boundary.centerx, self.boundary.centery)
            )
            surface.blit(msg_surf, msg_rect)

    def handle_event(self, event: pg.event.Event):
        if self.completed:
            return
        if self.state == "waiting" and self.start_button:  # waiting to start
            self.start_button.handle_event(event)
            if self.start_button.state == "DOWN":
                self.start_sequence()
                self.start_button.reset()

        elif self.state == "input":  # user input phase
            for btn in self.buttons:
                if btn.handle_event(event):
                    btn.flash()
                    self.user_input.append(btn.index)
                    if self.user_input[-1] != self.sequence[len(self.user_input) - 1]:
                        self.message = "Faux ! Recommence."
                        self.state = "waiting"
                        return
                    if len(self.user_input) == len(self.sequence):
                        self.message = "Bien joué !"
                        self.state = "finished"
                        return
