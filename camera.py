from math import sin, cos, tan, pi

class Camera:
    def __init__(self, x, y, z, screen_width, screen_height, fov=90, z_far=10, z_near=1):
        self.x = x
        self.y = y
        self.z = z
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fov = fov
        self.z_far = z_far
        self.z_near = z_near
    def get_projection_matrix(self):
        a = self.screen_height/self.screen_width
        f = 1/tan(self.fov*0.5*pi/180)
        q = self.z_far/(self.z_far-self.z_near)
        return [
            [a*f,   0,      0,             0],
            [0,     f,      0,             0],
            [0,     0,      q,             1],
            [0,     0,      q*self.z_near, 0],
        ]
    def get_rotation_z_matrix(self, angle):
        return [
            [ cos(angle), sin(angle), 0,  0],
            [-sin(angle), cos(angle), 0,  0],
            [ 0         , 0,          1,  0],
            [ 0         , 0,          0,  1],
        ]
    def get_rotation_y_matrix(self, angle):
        return [
            [cos(angle), 0 ,-sin(angle),   0],
            [0         , 1 , 0         ,   0],
            [sin(angle), 0 , cos(angle),   0],
            [0         , 0 , 0         ,   1],
        ]
    def get_rotation_x_matrix(self, angle):
        return [
            [1  , 0         , 0         ,   0],
            [0  , cos(angle), sin(angle),   0],
            [0  ,-sin(angle), cos(angle),   0],
            [0  , 0         , 0         ,   1],
        ]
    def update(self, dt, events):
        pass
