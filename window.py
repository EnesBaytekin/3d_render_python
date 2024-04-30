import pygame
from engine3d import Engine3D

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.SCALED)
        self.running = False
        self.engine3d = Engine3D(width, height)
    def mainloop(self):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            dt = clock.tick(60)/1000
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            self.engine3d.update(dt, events)
            self.screen.fill((0, 0, 0))
            self.engine3d.draw(self.screen)
            pygame.display.flip()
