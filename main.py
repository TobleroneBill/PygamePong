import math
import random
import pygame
import sys

HEIGHT, WIDTH = 1000, 800
CENTER = (HEIGHT // 2, WIDTH // 2)
SCREEN = pygame.display.set_mode((HEIGHT, WIDTH))
CLOCK = pygame.time.Clock()
FPS = 60
DefSpeed = 3    # Default ball speed

# this goes unused, because i didnt reaise this doesnt give you a normalized vector. The resulting angle needs to be
# normalized again i think, but also 0.0003 * 10, still makes 0.03, which is actually correct
# This is a wierd maths issue, that Idk about really. Think i can do the quake version now properly tho

# the formula to find the normalized direction is:
# tan(angle) = normalMag
# x = cos(angle)*normalMag
# y = sin(angle)*normalMag
def GetDirectionVector(angle):
    rng = random.randint(0, 2)
    if rng == 0:
        return 0, 0
    if rng == 1:
        return 1, 1
    angleInDegrees = math.degrees(angle)
    normalMag = math.tan(angleInDegrees)
    x = math.cos(angleInDegrees) * normalMag
    y = math.sin(angleInDegrees) * normalMag
    return x, y


# pythagoras. Not needed, but may be useful one day lol
def pythagoras(a, b):
    return math.sqrt((a * a) + (b * b))


# What does da ball do
class Ball:
    def __init__(self, pos, speed=10):
        self.x = pos[0]
        self.y = pos[1]
        self.speed = 5
        self.rect = pygame.rect.Rect((self.x, self.y), (10, 10))
        self.angle = 1
        self.up = True

    def move(self):
        # normalDir = GetDirectionVector(self.angle)
        # self.x += normalDir[0] * self.speed  # add x
        if self.up:
            self.y -= 1 * self.speed  # just swap this every collision, then just add a random x value to x
        else:
            self.y += 1 * self.speed
        self.x += self.angle
        self.rect.x = self.x
        self.rect.y = self.y

    def checkCollisions(self, p1, p2):
        if int(self.x) >= HEIGHT or self.x <= 0:  # if hits the side, reverse angle
            self.angle = -self.angle

        if self.y < -10:
            self.x = CENTER[0]
            self.y = CENTER[1]
            self.speed = DefSpeed
            p1.score += 1

        if self.y > WIDTH + 10:  # Resets ball
            self.x = CENTER[0]
            self.y = CENTER[1]
            self.speed = DefSpeed
            p2.score += 1

        # check if touching p1
        if p1.playerRect.colliderect(self.rect) or p2.playerRect.colliderect(self.rect):
            if self.speed <20:
                print(self.speed)
                self.speed += 1
            rng =  random.randint(0,10) * 0.1
            if random.randint(0,1) == 0:
                self.angle += rng
            else:
                self.angle -= rng
            print(f'new angle = {self.angle}')
            self.up = not self.up

    def draw(self):
        pygame.draw.ellipse(SCREEN, (255, 255, 255), self.rect)


class Player:
    def __init__(self, playerNum, pos):
        self.playerNum = playerNum  # player 1 or 2
        self.score = 0  # score
        self.size = (100, 10)  # paddle size
        self.pos = pos  # position on screen (only change x)
        self.speed = 10
        self.playerRect = pygame.Rect(self.pos, self.size)
        self.playerRect.center = self.pos  # aligns to center

    def checkMovement(self):  # check for player movement (check both and ball in a separate game function)
        if self.playerNum == 1:  # p1 control scheme
            self.move(pygame.K_a, pygame.K_d,pygame.KMOD_LSHIFT)
        if self.playerNum == 2:  # if player 2, use this control scheme
            self.move(pygame.K_LEFT, pygame.K_RIGHT,pygame.KMOD_RCTRL)

    def move(self, left, right,modifier):

        if pygame.key.get_mods() & modifier and pygame.key.get_pressed()[left]:         # if modifier down, move faster
            if not self.playerRect.left - self.speed < 0:  # edge check
                self.playerRect.left -= self.speed * 2
        elif pygame.key.get_pressed()[left]:
            if pygame.key.get_pressed()[left]:
                if not self.playerRect.left - self.speed < 0:  # edge check
                    self.playerRect.left -= self.speed

        if pygame.key.get_mods() & modifier and pygame.key.get_pressed()[right]:
            if self.playerRect.left + self.speed < HEIGHT - 90:
                self.playerRect.left += self.speed * 2
        else:
            if pygame.key.get_pressed()[right]:
                if self.playerRect.left + self.speed < HEIGHT - 90:
                    self.playerRect.left += self.speed

    def draw(self):
        pygame.draw.rect(SCREEN, (255, 255, 255), self.playerRect, 2)


def main():
    pygame.init()
    player1 = Player(1, (HEIGHT // 2, WIDTH - 50))  # Floor division for whole numbers
    player2 = Player(2, (HEIGHT // 2, 0 + 50))  # Floor division for whole numbers
    matchBall = Ball((HEIGHT // 2, WIDTH // 2), 1)  # place ball in center of screen
    playerfont = pygame.font.SysFont('Arial', 60, False, False)  # the font for text

    # Draws
    def MoveObjs():
        player1.checkMovement()
        player2.checkMovement()
        matchBall.checkCollisions(player1, player2)
        matchBall.move()

    def DrawScores():
        p1score = playerfont.render(str(player1.score), False, (255, 255, 255))  # render settings for the font
        SCREEN.blit(p1score, (HEIGHT // 2, WIDTH // 2))
        p2score = playerfont.render(str(player2.score), False, (255, 255, 255))  # render settings for the font
        SCREEN.blit(p2score, (HEIGHT // 2, (WIDTH // 2) - 70))

    def drawObjs():
        SCREEN.fill((0, 0, 0))
        DrawScores()
        pygame.draw.line(SCREEN, (255, 255, 255), (0, WIDTH // 2), (HEIGHT, WIDTH // 2), 5)
        player1.draw()
        player2.draw()
        matchBall.draw()
        MoveObjs()
        pygame.display.update()

    # Game loop
    while True:
        drawObjs()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
        # print(CLOCK.get_fps())
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
