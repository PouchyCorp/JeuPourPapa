from pygame import Surface, SRCALPHA, image, error, transform
import math

def load_image(path, scale = 1, size = None) -> Surface:
    try:
        img = image.load(path).convert_alpha()
        if scale != 1:
            img = transform.scale_by(img, scale)
        if size is not None:
            img = transform.scale(img, size)
        return img
    except error as e:
        print(f"Cannot load image: {path}")
        raise SystemExit(e)

class Spritesheet:
    def __init__(self, sprite : Surface, img_size : tuple[int]) -> None:
        """Initializes the spritesheet with the image and the size of the images in the spritesheet."""
        self.surf = sprite
        self.rect = self.surf.get_rect()
        self.img_size = img_size

    def get_img(self, coord : tuple[int]) -> Surface:
        """Returns the image at the given coordinates in the spritesheet."""
        coord_x_px = coord[0]*self.img_size[0] #take the last x-coord to calculate the next position
        coord_y_py = coord[1]*self.img_size[1] #take the last y-coord to calculate the next position
        try:
            # this is the normal efficient way to get the image
            return self.surf.subsurface((coord_x_px, coord_y_py, self.img_size[0], self.img_size[1])).copy() # return the image at the right position
        
        except ValueError: # if the image is out of the spritesheet, sometime happens when the animation is finished
            # this is the less efficient way to get the image, but it's the only way to avoid the ValueError for some images
            surf = Surface((self.img_size[0], self.img_size[1]), flags=SRCALPHA) # create a new surface with the right size
            surf.blit(self.surf, (0,0), (coord_x_px, coord_y_py, self.img_size[0], self.img_size[1])) # blit the image at the right position
            return surf
    
    def __getstate__(self):
        """Returns the state of the object for safely pickling.
        Needed because the Surface object cannot be pickled, so we convert it to a bytestring."""
        state = self.__dict__.copy()
        state["surf"] = (image.tostring(self.surf, "RGBA"), self.surf.get_size()) # convert the surface to a bytestring
        return state
    
    def __setstate__(self, state : dict):
        """Sets the state of the object after safely unpickling.
        Needed because the Surface object cannot be pickled, so we convert it back from a bytestring."""
        self.__dict__ = state 
        self.surf = image.frombuffer(self.surf[0], self.surf[1], "RGBA")  # convert the bytestring back to a surface


class Animation:
    def __init__(self, spritesheet : Spritesheet, line : int, length : int, speed : int = 6, repeat = True ) -> None:
        """Initializes the animation with the spritesheet, the line of the spritesheet to use, the number of frames in the animation, the speed of the animation, and whether the animation should repeat."""
        self.spritesheet = spritesheet
        self.img_index : int = 0
        self.line = line
        self.length = length
        self.speed = speed
        self.__speed_incr = 0
        self.repeat = repeat

    def get_frame(self) -> Surface:
        """returns the current frame of the animation and changes the frame if needed.  
        Needs to be called every frame to update the animation with the right speed."""
        if self.img_index == self.length-1 and self.repeat:
            self.img_index = 0
        
        # if the proper amount of skipped frames is reached, we change the frame
        if self.__speed_incr >= self.speed and self.img_index != self.length-1 :
            self.img_index += 1
            self.__speed_incr = 0
        else:
            self.__speed_incr += 1
        
        new_surf = self.spritesheet.get_img((self.img_index, self.line))
        return new_surf
    
    def reset_frame(self):
        """resets the animation to the first frame.  
        Can be useful for restarting the animation from the beginning
        returns 1st frame of the animation."""
        self.img_index = 0  

        new_surf = self.spritesheet.get_img((0, self.line))
        return new_surf
    
    def copy(self):
        return Animation(self.spritesheet,self.line,self.length,self.speed,self.repeat)

    def is_finished(self):
        """checks if the animation has reached its last frame."""
        if self.img_index == self.length-1 : #check if it's the last picture of the spritesheet
            return True
        
class ScreenFade:
    def __init__(self):
        self.playing = False
        self.incr = 0
        self.alpha = 0

    def draw(self, surface : Surface):
        if not self.playing:
            return
        fade_surf = Surface(surface.get_size(), flags=SRCALPHA)
        fade_surf.fill((0,0,0))
        fade_surf.set_alpha(self.alpha)
        surface.blit(fade_surf, (0,0))

    def update(self):
        if not self.playing:
            return
            
        self.incr += self.speed * math.pi
        if self.incr > self.stop:
            self.incr = 0
            self.playing = False
        self.alpha = int(math.sin(self.incr) * 255)

    def is_ascending(self):
        return self.incr < math.pi/2

    def start(self, speed: float, stop = math.pi, start = 0):
        self.playing = True
        self.alpha = 0
        self.incr = start
        self.speed = speed
        self.stop = stop
