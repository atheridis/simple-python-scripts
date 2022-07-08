import numpy as np
import pygame
import sys
# import cv2
import os
import math

RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

# out = cv2.VideoWriter('videos/Mandel0.avi',
#                        cv2.VideoWriter_fourcc(*'DIV4'),
#                        30, (1920, 1080))


class Lorenz:
    def __init__(self, X=0.1, Y=0.0, Z=0.1):
        self.X, self.Y, self.Z = X, Y, Z
        self.sigma, self.rho, self.beta = 10, 28, 8/3.0
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.dt = 0.01
        self.allpos = [self.current_pos()]

    def step(self):
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.X = self.X + self.dt * self.sigma * (self.Y - self.X)
        self.Y = self.Y + self.dt * (self.X * (self.rho - self.Z) - self.Y)
        self.Z = self.Z + self.dt * (self.X * self.Y - self.beta * self.Z)
        self.allpos.append(self.current_pos())

    def current_pos(self):
        return self.X, self.Y, self.Z

    def previous_pos(self):
        return self.oX, self.oY, self.oZ


class Screen:
    def __init__(self, maths):
        pygame.init()
        self.math = maths
        self.width = 1920
        self.height = 1080

        self.speed = 1

        self.camX = 30
        self.camY = 30
        self.camZ = 1

        self.cam_rot_X = 0
        self.cam_rot_Y = 0
        self.cam_rot_Z = 0

        self.frame = 0

        self.xMin, self.xMax = -30, 30
        self.yMin, self.yMax = -30, 30
        self.zMin, self.zMax = -5, 55

        self.screen = pygame.display.set_mode((self.width, self.height))

    def to_screen_units_XZ(self, x, z):
        screenX = self.width * (x - self.xMin) / (self.xMax - self.xMin)
        screenY = self.height * (self.zMax - z) / (self.zMax - self.zMin)

        return round(screenX), round(screenY)

    def to_screen_units_XY(self, x, y):
        screenX = self.width * (x - self.xMin) / (self.xMax - self.xMin)
        screenY = self.height * (self.yMax - y) / (self.yMax - self.yMin)

        return round(screenX), round(screenY)

    def to_screen_units_YZ(self, y, z):
        screenX = self.width * (y - self.yMin) / (self.yMax - self.yMin)
        screenY = self.height * (self.zMax - z) / (self.zMax - self.zMin)

        return round(screenX), round(screenY)

    def to_screen_units(self, x, y, z):
        z += self.camZ
        x += self.camX
        y += self.camY

        screen_pos = self.rot_z(-self.cam_rot_Z) @ self.rot_y(-self.cam_rot_Y) @ self.rot_x(-self.cam_rot_X) @ np.array([x, y, z])

        screenX = self.width * (1 + screen_pos[0] / 2) / (math.tan(math.pi / 4) * abs(screen_pos[2]))
        screenY = self.height * (1 + screen_pos[1] / 2) / (math.tan(9*math.pi / 64) * abs(screen_pos[2]))

        return [(round(screenX), round(screenY)), screen_pos[2]]

    def rot_x(self, angle):
        return np.array([[1.0, 0.0, 0.0],
                        [0.0, math.cos(angle), -math.sin(angle)],
                        [0.0, math.sin(angle), math.cos(angle)]])

    def rot_y(self, angle):
        return np.array([[math.cos(angle), 0.0, math.sin(angle)],
                        [0.0, 1.0, 0.0],
                        [-math.sin(angle), 0.0, math.cos(angle)]])

    def rot_z(self, angle):
        return np.array([[math.cos(angle), -math.sin(angle), 0.0],
                        [math.sin(angle), math.cos(angle), 0.0],
                        [0.0, 0.0, 1.0]])

    def draw_line(self):
        self.screen.fill((10,5,30))

        for m in self.math:
            prev_point = self.to_screen_units(m[0].allpos[0][0], m[0].allpos[0][1], m[0].allpos[0][2])
            for point in m[0].allpos:
                curr_point = self.to_screen_units(point[0], point[1], point[2])
                try:
                    if int(100 / max(curr_point[1], 0)) < 300 and prev_point[0][0] < 5000 and prev_point[0][1] < 5000 and curr_point[0][0] < 5000 and curr_point[0][1] < 5000:
                        pygame.draw.line(self.screen, self.color_intensity(max(curr_point[1], 0), m[1]), prev_point[0], curr_point[0], int(80 / max(curr_point[1], 0)))
                except ZeroDivisionError:
                    if prev_point[0][0] < 5000 and prev_point[0][1] < 5000 and curr_point[0][0] < 5000 and curr_point[0][1] < 5000:
                        pygame.draw.line(self.screen, self.color_intensity(max(curr_point[1], 0), m[1]), prev_point[0], curr_point[0], 0)
                prev_point = curr_point

            try:
                pygame.draw.circle(self.screen, self.color_intensity(max(curr_point[1], 0), m[1]), curr_point[0], int(100 / max(curr_point[1], 0)))
            except ZeroDivisionError:
                pygame.draw.circle(self.screen, self.color_intensity(max(curr_point[1], 0), m[1]), curr_point[0], 0)

    def color_intensity(self, dist, color):
        dist = min((abs(dist) / 100), 1)
        redness = color[0]
        greeness = color[1]
        blueness = color[2]
        redness = max(1 - dist, 0) * redness
        greeness = max(1 - dist, 0) * greeness
        blueness = max(1 - dist, 0) * blueness
        return int(redness), int(greeness), int(blueness)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                out.release()
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     self.speed = 3
        # if keys[pygame.K_w]:
        #     self.camZ -= 0.13 * self.speed
        # if keys[pygame.K_s]:
        #     self.camZ += 0.13 * self.speed
        # if keys[pygame.K_q]:
        #     self.camY -= 0.13 * self.speed
        # if keys[pygame.K_e]:
        #     self.camY += 0.13 * self.speed
        # if keys[pygame.K_a]:
        #     self.camX += 0.13 * self.speed
        # if keys[pygame.K_d]:
        #     self.camX -= 0.13 * self.speed
        # if keys[pygame.K_UP]:
        #     self.cam_rot_X += math.pi / 180
        # if keys[pygame.K_DOWN]:
        #     self.cam_rot_X -= math.pi / 180
        # if keys[pygame.K_LEFT]:
        #     self.cam_rot_Y += math.pi / 180
        # if keys[pygame.K_RIGHT]:
        #     self.cam_rot_Y -= math.pi / 180
        # if keys[pygame.K_RIGHTBRACKET]:
        #     self.cam_rot_Z += math.pi / 180
        # if keys[pygame.K_LEFTBRACKET]:
        #     self.cam_rot_Z -= math.pi / 180

        move = np.array([0.0, 0.0, 0.0])

        if keys[pygame.K_SPACE]:
            self.speed = 3
        if keys[pygame.K_w]:
            move[2] = -0.13 * self.speed
        if keys[pygame.K_s]:
            move[2] = 0.13 * self.speed
        if keys[pygame.K_q]:
            move[1] = -0.13 * self.speed
        if keys[pygame.K_e]:
            move[1] = 0.13 * self.speed
        if keys[pygame.K_a]:
            move[0] = 0.13 * self.speed
        if keys[pygame.K_d]:
            move[0] = -0.13 * self.speed

        move = self.rot_x(self.cam_rot_X) @ self.rot_y(self.cam_rot_Y) @ self.rot_z(self.cam_rot_Z) @ move

        if keys[pygame.K_UP]:
            self.cam_rot_X += math.pi / 180
        if keys[pygame.K_DOWN]:
            self.cam_rot_X -= math.pi / 180
        if keys[pygame.K_LEFT]:
            self.cam_rot_Y -= math.pi / 180
        if keys[pygame.K_RIGHT]:
            self.cam_rot_Y += math.pi / 180
        if keys[pygame.K_RIGHTBRACKET]:
            self.cam_rot_Z += math.pi / 180
        if keys[pygame.K_LEFTBRACKET]:
            self.cam_rot_Z -= math.pi / 180

        self.camX += move[0]
        self.camY += move[1]
        self.camZ += move[2]

        self.speed = 1

    def update(self):
        # for i in range(20):
        for m in self.math:
            m[0].step()

        # if self.frame % 10 == 0:
        #     print(self.camX, self.camY, self.camZ)
        #     print(self.cam_rot_X, self.cam_rot_Y, self.cam_rot_Z)
        pygame.display.flip()

        # if self.frame % 5 == 0:
        self.draw_line()
        #pygame.image.save(self.screen, "images/screen.png")
        #img = cv2.imread("images/screen.png")
        #os.remove("images/screen.png")
        #out.write(img)
        self.frame += 1

    def run(self):
        while True:
            self.handle_events()
            self.update()


if __name__ == "__main__":
    lorenz1 = Lorenz()
    lorenz2 = Lorenz(0.11, 0.0, 0.0)
    lorenz3 = Lorenz(0.09, 0.01, -0.01)
    lorenz = [(lorenz1, RED), (lorenz2, BLUE), (lorenz3, GREEN)]
    screen = Screen(lorenz)
    screen.run()
