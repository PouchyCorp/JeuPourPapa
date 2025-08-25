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
        if self.is_completed_countdown and self.fade_alpha == 255 and not screenshot_mode:
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
    def __init__(self, right_answer, possible_answers, correct_index, question: str = "Répond à la question !"):
        super().__init__(name="Quiz")
        self.question = question
        self.right_answer = right_answer
        self.possible_answers = possible_answers
        self.correct_index = correct_index
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
        spacing = 40

        total_width = num_answers * button_width + (num_answers - 1) * spacing
        start_x = self.boundary.centerx - total_width // 2
        y = self.boundary.bottom - button_height - 40

        for i, answer in enumerate(self.possible_answers):
            rect = pg.Rect(
                start_x + i * (button_width + spacing),
                y,
                button_width,
                button_height
            )
            button = Button(
                rect,
                answer,
                (255, 255, 255),
                36
            )
            self.buttons.append(button)

    def update(self):
        super().update()
        if self.completed:
            return

        if not self.buttons and self.boundary:
            self.setup()

        for button in self.buttons:
            if button.state == 'DOWN' and button.text == self.right_answer:
                self.is_completed_countdown = time() + 1

        for button in self.buttons:
            if button.state == 'DOWN' and button.last_pressed_time and time() - button.last_pressed_time >= 1:
                button.reset()
                break

    def draw(self, surface: pg.Surface, screenshot_mode=False):
        super().draw(surface, screenshot_mode)
        if self.completed and not screenshot_mode:
            return

        font = pg.font.SysFont("Arial", 48)
        question_surf = font.render(self.question, True, (255, 255, 255))
        question_rect = question_surf.get_rect(center=(self.boundary.centerx, self.boundary.top + 100))
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
        self.card_size = (100, 100)
        self.last_flip_time = None

    def setup(self):
        if not self.boundary or not self.images:
            return

        num_cards = self.grid_size[0] * self.grid_size[1]
        assert num_cards % 2 == 0, "Grid must have even number of cards"
        images = self.images * (num_cards // (2 * len(self.images)))
        images += random.sample(self.images, num_cards // 2 - len(images))
        images = images * 2
        random.shuffle(images)

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
                    start_x + x * (w + spacing),
                    start_y + y * (h + spacing),
                    w,
                    h
                )
                self.cards.append({
                    "rect": rect,
                    "image": images[idx],
                    "flipped": False,
                    "matched": False,
                    "index": idx
                })

    def update(self):
        super().update()
        if self.completed:
            return

        if not self.cards and self.boundary and self.images:
            self.setup()

        if len(self.flipped) == 2 and not self.last_flip_time:
            self.last_flip_time = time()

        if self.last_flip_time and time() - self.last_flip_time > 1:
            idx1, idx2 = self.flipped
            if self.cards[idx1]["image"] == self.cards[idx2]["image"]:
                self.cards[idx1]["matched"] = True
                self.cards[idx2]["matched"] = True
                self.matched.add(idx1)
                self.matched.add(idx2)
            self.cards[idx1]["flipped"] = False
            self.cards[idx2]["flipped"] = False
            self.flipped = []
            self.last_flip_time = None

        if all(card["matched"] for card in self.cards):
            self.is_completed_countdown = time() + 1

    def draw(self, surface: pg.Surface, screenshot_mode=False):
        super().draw(surface, screenshot_mode)
        if self.completed and not screenshot_mode:
            return

        font = pg.font.SysFont("Arial", 48)
        title_surf = font.render("Memory Game", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.boundary.centerx, self.boundary.top + 60))
        surface.blit(title_surf, title_rect)

        for card in self.cards:
            color = (200, 200, 200) if card["flipped"] or card["matched"] else (50, 50, 50)
            pg.draw.rect(surface, color, card["rect"])
            pg.draw.rect(surface, (255, 255, 255), card["rect"], 2)
            if card["flipped"] or card["matched"]:
                if isinstance(card["image"], pg.Surface):
                    img = pg.transform.scale(card["image"], (card["rect"].width - 10, card["rect"].height - 10))
                    surface.blit(img, (card["rect"].x + 5, card["rect"].y + 5))
                else:
                    img_font = pg.font.SysFont("Arial", 36)
                    img_surf = img_font.render(str(card["image"]), True, (0, 0, 0))
                    img_rect = img_surf.get_rect(center=card["rect"].center)
                    surface.blit(img_surf, img_rect)

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.USEREVENT + 0:
            pos = event.pos
            for idx, card in enumerate(self.cards):
                if card["rect"].collidepoint(pos) and not card["flipped"] and not card["matched"]:
                    card["flipped"] = True
                    self.flipped.append(idx)
                    if len(self.flipped) > 2:
                        # Should not happen, but reset if it does
                        for i in self.flipped:
                            self.cards[i]["flipped"] = False
                        self.flipped = [idx]
                    break



