import pygame
import math
from random import randint
pygame.init()

import globalConfig as cg
from ballLabelHandler import BallLabel
from ballLabelHandler import BallInfoBox

class Ball:
    def __init__(self, x, y, vx, vy, colour):
        self.x = x
        self.y = y
        self.radius = cg.ballRadius
        self.colour = colour
        self.vx = vx
        self.vy = vy
        self.mass = cg.ballRadius * 0.1
        self.volume = (4/3)*math.pi*(self.radius**3)
    
    def draw(self):
        pygame.draw.circle(cg.screen, self.colour, (int(self.x), int(self.y)), self.radius)
    
    def update(self, dt):
        self.vy += cg.gravity * dt
        
        self.x += self.vx * dt * cg.speed
        self.y += self.vy * dt * cg.speed
        
        if self.x - self.radius <= 0 or self.x + self.radius >= cg.SCREEN_WIDTH:
            self.vx = -self.vx * cg.friction
            if self.x - self.radius <= 0:
                self.x = self.radius
            else:
                self.x = cg.SCREEN_WIDTH - self.radius
        
        if self.y - self.radius <= 0 or self.y + self.radius >= cg.SCREEN_HEIGHT:
            self.vy = -self.vy * cg.friction
            if self.y - self.radius <= 0:
                self.y = self.radius
            else:
                self.y = cg.SCREEN_HEIGHT - self.radius

            self.vx *= cg.friction
            self.vy *= cg.friction

    def collide(self, other):
        # Calculate the distance between two balls
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.hypot(dx, dy)
        
        if dist < self.radius + other.radius:  # Collision detected
            # Swap velocities
            self.vx, other.vx = other.vx, self.vx
            self.vy, other.vy = other.vy, self.vy
            
            # Resolve overlap by pushing the balls apart
            overlap = 0.5 * (self.radius + other.radius - dist)
            angle = math.atan2(dy, dx)
            self.x -= overlap * math.cos(angle)
            self.y -= overlap * math.sin(angle)
            other.x += overlap * math.cos(angle)
            other.y += overlap * math.sin(angle)
            
    def keepOnScreenWhilePaused(self, dt):
        if self.x - self.radius <= 0 or self.x + self.radius >= cg.SCREEN_WIDTH:
            if self.x - self.radius <= 0:
                self.x = self.radius
            else:
                self.x = cg.SCREEN_WIDTH - self.radius
        
        if self.y - self.radius <= 0 or self.y + self.radius >= cg.SCREEN_HEIGHT:
            if self.y - self.radius <= 0:
                self.y = self.radius
            else:
                self.y = cg.SCREEN_HEIGHT - self.radius

def generateColours(num):
    colours = []
    for _ in range(num):
        colours.append((randint(0, 254), randint(0, 254), randint(0, 254)))
        
    return colours
       
def generateBalls():
    if cg.randomBallColours:
        generateBallsWithRandomColours()
        return
    
    cg.balls = [Ball(randint(50, cg.SCREEN_WIDTH-50), randint(50, cg.SCREEN_WIDTH-50), randint(-10, 10), randint(-5, 5), (255, 0, 0)) for _ in range(cg.ballNum//2)]
        
def generateBallsWithRandomColours():
    colours = generateColours(cg.ballNum)
    
    cg.balls = []
    for colour in colours:
        cg.balls.append(Ball(randint(50, cg.SCREEN_WIDTH-50), randint(50, cg.SCREEN_WIDTH-50), randint(-10, 10), randint(-5, 5), colour))
    
def checkForBallHover(mousePos):
    for ball in cg.balls:
        ballPos = (ball.x, ball.y)
        
        distance = math.sqrt((mousePos[0] - ballPos[0]) ** 2 + (mousePos[1] - ballPos[1]) ** 2)
        
        if distance <= ball.radius:
            ballInfo = getBallInfo(ball)
            
            BallLabel(ballInfo)
            
            break
            
def checkForBallClick(mousePos):
    for ball in cg.balls:
        ballPos = (ball.x, ball.y)
        
        distance = math.sqrt((mousePos[0] - ballPos[0]) ** 2 + (mousePos[1] - ballPos[1]) ** 2)
        
        if distance <= ball.radius:
            ballInfo = getBallInfo(ball)
            
            cg.showingBallInfoBox = [ball, BallInfoBox(ballInfo)]
            
            return True
   
def getBallInfo(ball):
    ballInfo = {}
    
    ballInfo["Pos"] = (ball.x, ball.y)
    ballInfo["Radius"] = ball.radius
    ballInfo["Colour"] = ball.colour
    ballInfo["Vel"] = (ball.vx, ball.vy)
    ballInfo["Mass"] = ball.mass
    ballInfo["Volume"] = ball.volume
    
    return ballInfo