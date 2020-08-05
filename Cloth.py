import pygame, sys, math

pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH), 0, 32)
pygame.display.set_caption('Cloth Physics')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
        self.newx = x
        self.newy = y
        self.ax = 0
        self.ay = 10

        self.fixed = False
        self.selected = False

    def update(self, delta_t):
        if self.fixed == False:
            # Verlet Integration
            self.newx = 2.0 * self.x - self.oldx + self.ax * delta_t * delta_t
            self.newy = 2.0 * self.y - self.oldy + self.ay * delta_t * delta_t
            self.oldx = self.x
            self.oldy = self.y
            self.x = self.newx
            self.y = self.newy

            # Collision Process
            if self.x < 0 or self.x > WIDTH:
                self.x, self.oldx = self.oldx, self.x
            if self.y < 0 or self.y > WIDTH:
                self.y, self.oldy = self.oldy, self.y

        if self.selected == True:
            pos = pygame.mouse.get_pos()
            self.x = pos[0]
            self.y = pos[1]
        if mouse == False:
            self.selected = False

    def draw(self, surf, size):
        if self.selected == True:
            color = RED
        else:
            color = WHITE
        pygame.draw.circle(surf, color, (int(self.x), int(self.y)), size)

class Constraint:
    def __init__(self, index0, index1):
        self.index0 = index0
        self.index1 = index1
        delta_x = particles[self.index0].x - particles[self.index1].x
        delta_y = particles[self.index0].y - particles[self.index1].y
        self.restLength = math.sqrt(delta_x * delta_x + delta_y * delta_y)

    def update(self):
        delta_x = particles[self.index1].x - particles[self.index0].x
        delta_y = particles[self.index1].y - particles[self.index0].y
        deltaLength = math.sqrt(delta_x * delta_x + delta_y * delta_y)
        diff = (deltaLength - self.restLength)/deltaLength

        if particles[self.index0].fixed == False:
            particles[self.index0].x += 0.5 * diff * delta_x
            particles[self.index0].y += 0.5 * diff * delta_y
        if particles[self.index1].fixed == False:
            particles[self.index1].x -= 0.5 * diff * delta_x
            particles[self.index1].y -= 0.5 * diff * delta_y

    def draw(self, surf, size):
        x0 = particles[self.index0].x
        y0 = particles[self.index0].y
        x1 = particles[self.index1].x
        y1 = particles[self.index1].y
        pygame.draw.line(surf, WHITE, (int(x0), int(y0)), (int(x1), int(y1)), size)


def find_particle(pos):
    for i in range(len(particles)):
        dx = particles[i].x - pos[0]
        dy = particles[i].y - pos[1]
        if (dx*dx + dy*dy) < 400:
            particles[i].selected = True
            break

delta_t = 0.1
mouse = False

# create particles
NUM_X = 15
NUM_Y = 15
particles = []
for j in range(NUM_Y):
    for i in range(NUM_X):
        x = 100 + i * 20.0
        y = j * 20.0
        p = Particle(x, y)
        particles.append(p)

particles[0].fixed = True
particles[NUM_X-1].fixed = True

constraints = []
for j in range(NUM_Y):
    for i in range(NUM_X):
        if i < (NUM_X - 1):
            index0 = i + j * NUM_X
            index1 = (i + 1) + j * NUM_X
            c = Constraint(index0, index1)
            constraints.append(c)
        if j < (NUM_Y - 1):
            index0 = i + j * NUM_Y
            index1 = i + (j + 1) * NUM_Y
            c = Constraint(index0, index1)
            constraints.append(c)

while True:
    WIN.fill(BLACK)

    for p in particles:
        p.update(delta_t)

    for c in constraints:
        c.update()

    for p in particles:
        p.draw(WIN, 3)

    for c in constraints:
        c.draw(WIN, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = False

    if mouse:
        pos = pygame.mouse.get_pos()
        find_particle(pos)

    pygame.display.update()
    fpsClock.tick(FPS)
