# Modular Minigame System Documentation

## Overview

The modular minigame system allows you to create various types of interactive challenges linked to puzzle pieces. When a player interacts with a puzzle piece, the associated minigame is activated.

## Core Classes

### `MinigameBase` (Abstract)
The base class that all minigames must inherit from. Provides the core interface and lifecycle management.

### `GenericMinigame`
A highly configurable minigame that can be customized for different types of challenges without creating new classes.

### `SimpleClickMinigame`
A concrete example implementation where the player must click a button a certain number of times.

## Usage Examples

### 1. Simple Click Minigame
```python
# Create a minigame where the player needs to click 5 times
minigame = SimpleClickMinigame(puzzle_piece, required_clicks=5)
puzzle_manager.add_minigame(puzzle_piece, minigame)
```

### 2. Generic Button-Based Minigame
```python
minigame = GenericMinigame(puzzle_piece, "Solve the Puzzle")

# Add a button that completes the minigame when clicked
button_rect = pg.Rect(200, 200, 150, 80)
minigame.add_button_config(button_rect, "Solve!", lambda: minigame.complete_minigame())

# Set a custom win condition (optional, button action will complete it)
minigame.set_win_condition(lambda: False)

puzzle_manager.add_minigame(puzzle_piece, minigame)
```

### 3. Time-Based Minigame
```python
minigame = GenericMinigame(puzzle_piece, "Wait 3 Seconds")

start_time = [0]  # Use list for mutable reference

def setup_timer():
    start_time[0] = pg.time.get_ticks()

def check_timer():
    return pg.time.get_ticks() - start_time[0] > 3000  # 3 seconds

minigame.set_custom_update(setup_timer)
minigame.set_win_condition(check_timer)

puzzle_manager.add_minigame(puzzle_piece, minigame)
```

### 4. Custom Drawing Minigame
```python
minigame = GenericMinigame(puzzle_piece, "Custom Display")

def custom_draw(surface):
    # Draw custom elements
    pg.draw.circle(surface, (255, 0, 0), (400, 300), 50)
    
    # Draw instructions
    font = pg.font.SysFont("Arial", 24)
    text = font.render("Complete the challenge!", True, (255, 255, 255))
    surface.blit(text, (300, 200))

minigame.set_custom_draw(custom_draw)

puzzle_manager.add_minigame(puzzle_piece, minigame)
```

## System Integration

### In PuzzleManager
The `PuzzleManager` handles:
- Storing minigames linked to puzzle pieces
- Starting minigames when pieces are interacted with
- Managing the active minigame
- Updating and drawing minigames
- Event routing

### In Main Game Loop
```python
# In handle_events()
if self.puzzle_manager.handle_event(event):
    continue  # Event was handled by puzzle manager

# In update()
self.puzzle_manager.update()

# In draw()
self.puzzle_manager.draw(surface)  # Draws pieces and active minigame
```

## Creating Custom Minigames

To create a completely custom minigame, inherit from `MinigameBase`:

```python
class MyCustomMinigame(MinigameBase):
    def setup(self):
        # Initialize your minigame
        pass
    
    def check_win_condition(self) -> bool:
        # Return True when the player has won
        return False
    
    def update(self):
        # Update game logic each frame
        pass
    
    def draw(self, surface: pg.Surface):
        # Draw your minigame elements
        pass
    
    def handle_event(self, event: pg.event.Event):
        # Handle input events
        pass
```

## Key Features

1. **Automatic Puzzle Piece Collection**: When a minigame is completed, the linked puzzle piece automatically starts its collection animation.

2. **Overlay System**: Active minigames display with a semi-transparent overlay and title.

3. **Event Isolation**: The system ensures minigame events don't interfere with normal gameplay.

4. **Modular Design**: Easy to add new minigame types without modifying existing code.

5. **State Management**: Each minigame tracks its own state and completion status.
