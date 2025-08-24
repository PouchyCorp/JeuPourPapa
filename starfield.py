import pygame as pg
import random
from typing import List, Tuple


class Star:
    """Represents a single star in the starfield."""
    
    def __init__(self, x: float, y: float, speed: float, brightness: int, size: int = 1, twinkle: bool = False):
        self.x = x
        self.y = y
        self.speed = speed
        self.base_brightness = brightness  # Base brightness value
        self.current_brightness = brightness
        self.size = size
        self.twinkle = twinkle
        self.twinkle_timer = random.random() * 60  # Random phase for twinkling
        self.color = (brightness, brightness, brightness)
    
    def update(self, screen_height: int, screen_width: int) -> None:
        """Update star position and twinkling effect."""
        self.y += self.speed
        
        # Reset star to top when it goes off the bottom
        if self.y > screen_height + 10:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, screen_width)
        
        # Handle twinkling effect
        if self.twinkle:
            self.twinkle_timer += 0.1
            # Create a subtle brightness variation
            variation = int(20 * abs(pg.math.Vector2(1, 0).rotate(self.twinkle_timer * 180).x))
            self.current_brightness = max(0, min(255, self.base_brightness + variation - 10))
            self.color = (self.current_brightness, self.current_brightness, self.current_brightness)
    
    def draw(self, surface: pg.Surface) -> None:
        """Draw the star on the surface."""
        if self.size == 1:
            # Single pixel star
            if 0 <= self.x < surface.get_width() and 0 <= self.y < surface.get_height():
                surface.set_at((int(self.x), int(self.y)), self.color)
        else:
            # Multi-pixel star (circle)
            if 0 <= self.x < surface.get_width() and 0 <= self.y < surface.get_height():
                pg.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class Starfield:
    """Manages a collection of stars creating a starfield effect."""
    
    def __init__(self, screen_width: int, screen_height: int, num_stars: int = 200):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.stars: List[Star] = []
        
        # Create initial stars scattered across the screen
        for _ in range(num_stars):
            self._create_random_star(initial_scatter=True)
    
    def _create_random_star(self, initial_scatter: bool = False) -> None:
        """Create a single random star."""
        x = random.randint(0, self.screen_width)
        
        if initial_scatter:
            # For initial setup, scatter stars across the entire screen
            y = random.randint(0, self.screen_height)
        else:
            # For new stars during gameplay, start them above the screen
            y = random.randint(-self.screen_height, self.screen_height)
        
        # Vary speed (slower stars are further away)
        speed = random.uniform(0.3, 3.5)
        
        # Vary brightness (dimmer stars are further away, brighter ones closer)
        # Bias toward dimmer stars for more realistic effect
        brightness_roll = random.random()
        twinkle = False
        
        if brightness_roll < 0.7:  # 70% dim stars
            brightness = random.randint(40, 100)
            size = 1
        elif brightness_roll < 0.9:  # 20% medium stars
            brightness = random.randint(100, 180)
            size = random.choice([1, 2])
            twinkle = random.random() < 0.3  # 30% chance to twinkle
        else:  # 10% bright stars
            brightness = random.randint(180, 255)
            size = random.choice([2, 3])
            twinkle = random.random() < 0.7  # 70% chance to twinkle
        
        star = Star(x, y, speed, brightness, size, twinkle)
        self.stars.append(star)
    
    def update(self) -> None:
        """Update all stars in the starfield."""
        for star in self.stars:
            star.update(self.screen_height, self.screen_width)
    
    def draw(self, surface: pg.Surface) -> None:
        """Draw all stars on the surface."""
        for star in self.stars:
            star.draw(surface)
    
    def add_star(self) -> None:
        """Add a new random star to the field."""
        self._create_random_star(initial_scatter=False)
    
    def remove_star(self) -> None:
        """Remove a star from the field."""
        if self.stars:
            self.stars.pop()
    
    def set_star_count(self, count: int) -> None:
        """Set the total number of stars."""
        current_count = len(self.stars)
        
        if count > current_count:
            # Add stars (new stars start above screen during gameplay)
            for _ in range(count - current_count):
                self.add_star()
        elif count < current_count:
            # Remove stars
            self.stars = self.stars[:count]
