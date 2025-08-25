import pygame as pg
from puzzlepiece import PuzzlePiece
from time import time

class GenericQuiz:
    def __init__(self, right_answer, possible_answers, correct_index, question: str = "Répond à la question !"):
        self.boundary = None  # Will be set by PuzzleManager
        self.completed = False  # Changed from is_completed to match PuzzleManager expectations
        self.question = question
        self.right_answer = right_answer
        self.possible_answers = possible_answers
        self.correct_index = correct_index
        self.is_completed_countdown = None
        self.fade_alpha = 255
        self.buttons = []
        self.name = "Quiz"  # Add name attribute for PuzzleManager compatibility

    def setup(self):
        if not self.boundary:
            return  # Can't setup without boundary
            
        from Button import Button  # Import here to avoid circular imports
        from globalSurfaces import BUTTON_UP

        self.buttons: list[Button] = []
        num_answers = len(self.possible_answers)
        button_width = BUTTON_UP.get_width()
        button_height = BUTTON_UP.get_height()
        spacing = 40

        total_width = num_answers * button_width + (num_answers - 1) * spacing
        start_x = self.boundary.centerx - total_width // 2
        y = self.boundary.bottom - button_height - 40  # 40px margin from bottom

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
                (255, 255, 255),  # white text
                36  # font size
            )
            self.buttons.append(button)
    
    def update(self):
        if self.completed:
            return
        
        if self.is_completed_countdown and time() >= self.is_completed_countdown:
            self.completed = True
            return
        
        # Setup buttons if not already done
        if not self.buttons and self.boundary:
            self.setup()
        
        # Check win condition
        for button in self.buttons:
            if button.state == 'DOWN' and button.text == self.right_answer:
                self.is_completed_countdown = time() + 1  # 1 second countdown to mark as completed
                # TODO: play success sound
        
        # Update buttons
        for button in self.buttons:
            if button.state == 'DOWN' and button.last_pressed_time and time() - button.last_pressed_time >= 1:
                button.reset()  # Reset all buttons after 1000ms
                break

    def draw(self, surface: pg.Surface, screenshot_mode=False):
        if self.is_completed_countdown and self.fade_alpha == 255 and not screenshot_mode: # Just completed
            self.minigame_screenshot = pg.Surface(surface.get_size(), pg.SRCALPHA)
            self.draw(self.minigame_screenshot, screenshot_mode=True) # Use screenshot mode to avoid recursion (this is made to have a general solution not just for quiz)
            self.fade_alpha -= 1 # Start fading out

        if self.is_completed_countdown and self.fade_alpha > 0 and not screenshot_mode: # Fading out
            self.fade_alpha -= 5
            self.minigame_screenshot.set_alpha(self.fade_alpha)
            surface.blit(self.minigame_screenshot, (0,0))

            if self.fade_alpha <= 0: # Fully faded out
                self.fade_alpha = 0
                self.completed = True
            return
        elif self.completed and not screenshot_mode: # Fully faded out
            return
        
        # Draw the question text
        font = pg.font.SysFont("Arial", 48)
        question_surf = font.render(self.question, True, (255, 255, 255))
        question_rect = question_surf.get_rect(center=(self.boundary.centerx, self.boundary.top + 100))
        surface.blit(question_surf, question_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
    
    def handle_event(self, event: pg.event.Event):
        if self.completed:
            return
        
        # Handle button events
        for button in self.buttons:
            button.handle_event(event)