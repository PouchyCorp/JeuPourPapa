import pygame as pg
from puzzlepiece import PuzzlePiece


class GenericQuiz:
    def __init__(self, right_answer, possible_answers, correct_index, question: str = "Répond à la question !"):
        self.boundary = None  # Will be set by PuzzleManager
        self.completed = False  # Changed from is_completed to match PuzzleManager expectations
        self.question = question
        self.right_answer = right_answer
        self.possible_answers = possible_answers
        self.correct_index = correct_index
        self.buttons = []
        self.name = "Quiz"  # Add name attribute for PuzzleManager compatibility

    def setup(self):
        if not self.boundary:
            return  # Can't setup without boundary
            
        from puzzlemanager import Button  # Import here to avoid circular imports
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
        
        # Setup buttons if not already done
        if not self.buttons and self.boundary:
            self.setup()
        
        # Check win condition
        for button in self.buttons:
            if button.state == 'DOWN' and button.text == self.right_answer:
                self.completed = True
        
        # Update buttons
        for button in self.buttons:
            if button.state == 'DOWN':
                pg.time.set_timer(pg.USEREVENT + 1, 1000)  # Reset all buttons after 1000ms
                break

    def draw(self, surface: pg.Surface):
        if self.completed:
            return
        
        # Draw the question text
        font = pg.font.SysFont("Arial", 48)
        question_surf = font.render(self.question, True, (255, 255, 255))
        question_rect = question_surf.get_rect(center=(surface.get_width() // 2, 200))
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