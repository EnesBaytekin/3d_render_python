from object import Object
from camera import Camera

class Engine3D:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.objects = [
            Object(0, 0, 3),
        ]

        self.camera = Camera(0, 0, 0, screen_width, screen_height)
    def draw(self, screen):
        for object in self.objects:
            object.draw(screen, self.camera)
    def update(self, dt, events):
        for object in self.objects:
            object.update(dt, events)
