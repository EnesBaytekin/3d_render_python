from triangle import Triangle
from util import *
from math import sqrt

from camera import Camera

class Object:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vertices = []
        self.triangles = []
        self.load_3d_shape("objects/a.obj")
        
        self.theta_x = 0
        self.theta_y = 0
        self.theta_z = 0
    def load_3d_shape(self, file_name):
        self.vertices.clear()
        self.triangles.clear()
        with open(file_name, "r") as obj_file:
            for line in obj_file.readlines():
                elements = line.strip().split()
                # print(elements)
                if elements[0] == "v":
                    vertex = [
                        float(elements[1]),
                        float(elements[2]),
                        float(elements[3]),
                    ]
                    self.vertices.append(vertex)
                if elements[0] == "f":
                    vertices = [
                        self.vertices[int(elements[1])-1],
                        self.vertices[int(elements[2])-1],
                        self.vertices[int(elements[3])-1],
                    ]
                    self.triangles.append(Triangle(*vertices))
        #region
        # self.vertices = [
        #     [-1, -1, -1],
        #     [-1, -1,  1],
        #     [-1,  1, -1],
        #     [-1,  1,  1],
        #     [ 1, -1, -1],
        #     [ 1, -1,  1],
        #     [ 1,  1, -1],
        #     [ 1,  1,  1],
        # ]
        # self.triangles = [
        #     Triangle(self.vertices[0], self.vertices[2], self.vertices[6]),
        #     Triangle(self.vertices[0], self.vertices[6], self.vertices[4]),
        #     Triangle(self.vertices[4], self.vertices[6], self.vertices[7]),
        #     Triangle(self.vertices[4], self.vertices[7], self.vertices[5]),
        #     Triangle(self.vertices[5], self.vertices[7], self.vertices[3]),
        #     Triangle(self.vertices[5], self.vertices[3], self.vertices[1]),
        #     Triangle(self.vertices[1], self.vertices[3], self.vertices[2]),
        #     Triangle(self.vertices[1], self.vertices[2], self.vertices[0]),
        #     Triangle(self.vertices[2], self.vertices[3], self.vertices[7]),
        #     Triangle(self.vertices[2], self.vertices[7], self.vertices[6]),
        #     Triangle(self.vertices[0], self.vertices[4], self.vertices[5]),
        #     Triangle(self.vertices[0], self.vertices[5], self.vertices[1]),
        # ]
        #endregion
    def draw(self, screen, camera: Camera):
        # triangles_to_draw = []
        for triangle in self.triangles:
            triangle_translated = Triangle((0, 0), (0, 0), (0, 0))
            for i, vertex in enumerate(triangle.vertices):
                vector = [*vertex, 1]
                # rotate
                vector = multiply_vector_matrix(vector, camera.get_rotation_x_matrix(self.theta_x))
                vector = multiply_vector_matrix(vector, camera.get_rotation_y_matrix(self.theta_y))
                vector = multiply_vector_matrix(vector, camera.get_rotation_z_matrix(self.theta_z))
                # move
                vector[0] += self.x
                vector[1] += self.y
                vector[2] += self.z
                triangle_translated.vertices[i] = [vector[0], vector[1], vector[2]]
            # calculate normal
            line1 = [
                triangle_translated.vertices[1][0]-triangle_translated.vertices[0][0],
                triangle_translated.vertices[1][1]-triangle_translated.vertices[0][1],
                triangle_translated.vertices[1][2]-triangle_translated.vertices[0][2],
            ]
            line2 = [
                triangle_translated.vertices[2][0]-triangle_translated.vertices[0][0],
                triangle_translated.vertices[2][1]-triangle_translated.vertices[0][1],
                triangle_translated.vertices[2][2]-triangle_translated.vertices[0][2],
            ]
            normal = [
                line1[1]*line2[2]-line1[2]*line2[1],
                line1[2]*line2[0]-line1[0]*line2[2],
                line1[0]*line2[1]-line1[1]*line2[0],
            ]
            normal_length = sqrt(normal[0]**2+normal[1]**2+normal[2]**2)
            normal[0] /= normal_length
            normal[1] /= normal_length
            normal[2] /= normal_length
            translated_vector = [
                triangle_translated.vertices[0][0]-camera.x,
                triangle_translated.vertices[0][1]-camera.y,
                triangle_translated.vertices[0][2]-camera.z,
            ]
            translated_vector_length = sqrt(translated_vector[0]**2+translated_vector[1]**2+translated_vector[2]**2)
            translated_vector[0] /= translated_vector_length
            translated_vector[1] /= translated_vector_length
            translated_vector[2] /= translated_vector_length
            dot_product = (
                normal[0]*translated_vector[0]+
                normal[1]*translated_vector[1]+
                normal[2]*translated_vector[2]
            )
            if dot_product < 0:
                # light
                light_direction = [0, 0, -1]
                light_direction_length = sqrt(light_direction[0]**2+light_direction[1]**2+light_direction[2]**2)
                light_direction[0] /= light_direction_length
                light_direction[1] /= light_direction_length
                light_direction[2] /= light_direction_length
                dp = (
                    normal[0]*light_direction[0]+
                    normal[1]*light_direction[1]+
                    normal[2]*light_direction[2]
                )
                color = (
                    min(max(dp, 0), 1)*255,
                    min(max(dp, 0), 1)*255,
                    min(max(dp, 0), 1)*255,
                )
                projected_points = []
                # center = [0, 0, 0]
                for vertex in triangle_translated.vertices:
                    # center[0] += vertex[0]
                    # center[1] += vertex[1]
                    # center[2] += vertex[2]
                    # convert to 2d
                    vector = [*vertex, 1]
                    vector = multiply_vector_matrix(vector, camera.get_projection_matrix())
                    x, y, z, w = vector
                    if w != 0:
                        x /= w
                        y /= w
                        z /= w
                    #scale to the screen size
                    x = (x+1)*0.5*camera.screen_width
                    y = (y+1)*0.5*camera.screen_height
                    projected_points.append([x, y])
                # distance = sqrt(
                #     (center[0]-camera.x)**2+
                #     (center[1]-camera.y)**2+
                #     (center[2]-camera.z)**2
                # )
                # triangles_to_draw.append([projected_points, color, distance])
                draw_triangle(screen, *projected_points, color)
                # draw_triangle(screen, *projected_points, (192, 0, 0), 1)
        # for triangle in sorted(triangles_to_draw, key=lambda triangle: triangle[2], reverse=True):
        #     draw_triangle(screen, *triangle[0], color)
    def update(self, dt, events):
        pressed_keys = pygame.key.get_pressed()
        self.theta_x += dt*(pressed_keys[pygame.K_i]-pressed_keys[pygame.K_k])
        self.theta_z += dt*(pressed_keys[pygame.K_l]-pressed_keys[pygame.K_j])
        self.x += 2*dt*(pressed_keys[pygame.K_d]-pressed_keys[pygame.K_a])
        self.y += 2*dt*(pressed_keys[pygame.K_LSHIFT]-pressed_keys[pygame.K_SPACE])
        self.z += 2*dt*(pressed_keys[pygame.K_w]-pressed_keys[pygame.K_s])
