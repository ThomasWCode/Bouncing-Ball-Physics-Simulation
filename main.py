import pygame
from random import randint
pygame.init()

from simInfoInputHandler import SimInfoInputHandler
SimInfoInputHandler()

import globalConfig as cg
cg.screen = pygame.display.set_mode((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT))
pygame.display.set_caption("Physics Ball Simulator")

import ballHandler
import inputGuiHandler as InputGuiHandler
import ballLabelHandler

#COLOURS
WHITE = (255, 255, 255)

ballHandler.generateBalls()

def reset():
    cg.resetAll()
    
    SimInfoInputHandler()
    
    cg.screen = pygame.display.set_mode((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT))
    pygame.display.set_caption("Physics Ball Simulator")
    
    ballHandler.generateBalls()
    
    startRunningSim()

def startRunningSim():
    clock = pygame.time.Clock()
    startTicks = pygame.time.get_ticks()
    frameCount = 0
    running = True
    while running:
        if cg.reset:
            running = False
            reset()
            break
        
        dt = clock.tick(cg.targetFPS) / 1000

        for event in pygame.event.get():
            mousePos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                continue
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressedButton = InputGuiHandler.mouseDown(mousePos)
                
                if not pressedButton:
                    ballClicked = ballHandler.checkForBallClick(mousePos)
                    
                if not pressedButton and not ballClicked and cg.showingBallInfoBox[0]:
                    cg.showingBallInfoBox[1].checkForClickOfInfoBox(mousePos)
                
            elif cg.usingSpeedSlider and event.type == pygame.MOUSEMOTION:
                InputGuiHandler.adjustSpeedSlider(mousePos)
                
            elif cg.usingSpeedSlider and event.type == pygame.MOUSEBUTTONUP:
                cg.usingSpeedSlider = False
        
        if not cg.paused:
            cg.screen.fill(WHITE)
                
            # Update and draw each ball
            for ball in cg.balls:
                ball.update(dt)
                ball.draw()
                
            InputGuiHandler.drawDefaultInputGuis()
            
            if not cg.usingSpeedSlider and not cg.showingBallInfoBox[0]:
                ballHandler.checkForBallHover(mousePos)
                
            if cg.showingBallInfoBox[0]:
                ballInfo = ballHandler.getBallInfo(ball)
            
                ballLabelHandler.BallInfoBox(ballInfo)
            
            # Check for collisions between balls
            for i in range(len(cg.balls)):
                for j in range(i + 1, len(cg.balls)):  # Avoid checking the same pair twice
                    cg.balls[i].collide(cg.balls[j])
                    
        else:
            cg.screen.fill(WHITE)
            
            # Update (with paused func) and draw each ball
            for ball in cg.balls:
                ball.keepOnScreenWhilePaused(dt)
                ball.draw()
            
            InputGuiHandler.drawDefaultInputGuis()
        
            if not cg.usingSpeedSlider and not cg.showingBallInfoBox[0]:
                ballHandler.checkForBallHover(mousePos)
                
            if cg.showingBallInfoBox[0]:
                ballInfo = ballHandler.getBallInfo(ball)
            
                ballLabelHandler.BallInfoBox(ballInfo)
            
        pygame.display.update()
        
        frameCount += 1
        if pygame.time.get_ticks() - startTicks >= 1000:  # Every second
            cg.currentFPS = frameCount
            
            frameCount = 0
            startTicks = pygame.time.get_ticks()
            
startRunningSim()