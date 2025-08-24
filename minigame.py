import pygame as pg
from puzzlepiece import PuzzlePiece

class GenericQuiz:
    """
    A generic, configurable minigame that can be customized for different puzzle pieces.
    """
    
    def __init__(self, linked_puzzle_piece: PuzzlePiece, question: str = "Répond à la question !"):
        self.linked_puzzle_piece = linked_puzzle_piece
        self.is_active = False
        self.is_completed = False
        self.question = question
        self.button_configurations = []
        self.win_condition_func = None
        self.custom_draw_func = None
        self.custom_update_func = None
        self.custom_event_handler = None
        
    def add_button_config(self, rect: pg.Rect, text: str = '', action = None, 
                         text_color: tuple = (0, 0, 0), font_size: int = 30):
        """Add a button configuration to be created during setup."""
        self.button_configurations.append({
            'rect': rect,
            'text': text,
            'action': action,
            'text_color': text_color,
            'font_size': font_size
        })
    
    def set_win_condition(self, condition_func):
        """Set the win condition function."""
        self.win_condition_func = condition_func
    
    def set_custom_draw(self, draw_func):
        """Set a custom drawing function."""
        self.custom_draw_func = draw_func
    
    def set_custom_update(self, update_func):
        """Set a custom update function."""
        self.custom_update_func = update_func

    def set_custom_event_handler(self, event_handler):
        """Set a custom event handler."""
        self.custom_event_handler = event_handler
    
    def setup(self):
        """Initialize the minigame with configured buttons and settings."""
        from puzzlemanager import Button  # Import here to avoid circular imports
        
        # Create buttons from configurations
        self.buttons : list[Button] = []
        for config in self.button_configurations:
            button = Button(
                config['rect'],
                config['text'],
                config['text_color'],
                config['font_size']
            )
            self.buttons.append(button)
    
    def check_win_condition(self) -> bool:
        """Check if the win condition has been met."""
        if self.win_condition_func:
            return self.win_condition_func()
        return False
    
    def update(self):
        """Update the minigame logic each frame."""
        if not self.is_active or self.is_completed:
            return
        
        # Check win condition
        if self.check_win_condition():
            self.complete_minigame()
            return
        
        # Run custom update function if provided
        if self.custom_update_func:
            self.custom_update_func()
        
        # Update buttons
        for button in self.buttons:
            # Reset button states if needed (you might want to customize this)
            if button.state == 'DOWN':
                button.reset()
    
    def draw(self, surface: pg.Surface):
        """Draw the minigame elements to the surface."""
        if not self.is_active:
            return
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
        
        # Run custom draw function if provided
        if self.custom_draw_func:
            self.custom_draw_func(surface)
    
    def handle_event(self, event: pg.event.Event):
        """Handle input events for the minigame."""
        if not self.is_active or self.is_completed:
            return
        
        # Handle button events
        for button in self.buttons:
            if button.is_clicked(event):
                button.handle_event(event)
        
        # Run custom event handler if provided
        if self.custom_event_handler:
            self.custom_event_handler(event)