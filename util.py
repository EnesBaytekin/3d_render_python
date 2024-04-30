import pygame
import pygame.draw

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def multiply_vector_matrix(v, m):
    result = []
    for i in range(len(m[0])):
        value = 0
        for j in range(len(v)):
            value += v[j]*m[j][i]
        result.append(value)
    return result

def draw_triangle(screen, p1, p2, p3, color, width=0):
    # pygame.draw.line(screen, color, p1, p2)
    # pygame.draw.line(screen, color, p2, p3)
    # pygame.draw.line(screen, color, p3, p1)
    pygame.draw.polygon(screen, color, (p1, p2, p3), width)
