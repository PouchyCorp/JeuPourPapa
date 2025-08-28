import pygame


class camera_class:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.screen = pygame.Surface((rect.width, rect.height))

    def reset_screen(self):  # must be called
        self.screen.fill("black")

    def show_on_camera(
        self, image: pygame.Surface, destination: pygame.Rect | tuple[int, int]
    ):
        if isinstance(destination, tuple):
            destination = image.get_rect(x=destination[0], y=destination[1])

        relative_destination = pygame.Rect(
            destination.x - self.rect.x,
            destination.y - self.rect.y,
            destination.width,
            destination.height,
        )

        if self.rect.colliderect(
            destination
        ):  # check if it's in the screen (optimization)
            self.screen.blit(image, relative_destination)


def camera_init(screen: pygame.Surface):
    """
    must be called after screen init"""
    global camera

    camera = camera_class(pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
    return camera


def show(image: pygame.Surface, destination: pygame.Rect | tuple[int, int]):
    """
    make an image appering to camera
    """

    if isinstance(destination, tuple):
        destination = image.get_rect(x=destination[0], y=destination[1])

    camera.show_on_camera(image, destination)
