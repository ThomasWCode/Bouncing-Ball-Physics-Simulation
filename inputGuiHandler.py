import pygame
import math
pygame.init()

import globalConfig as cg

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)

#FONTS
fpsLabelFont = pygame.font.Font(None, 32)
resetLabelFont = pygame.font.Font(None, 25)

#VARS
speedSliderPos = None
speedSliderKnobRadius = 15
speedSliderLength = 200

playButtonImage = pygame.image.load("Images/playButton.png").convert_alpha()
playButtonImage = pygame.transform.scale(playButtonImage, (50, 50))
playButtonRect = pygame.rect.Rect(cg.SCREEN_WIDTH-50, 0, 50, 50)

pauseButtonImage = pygame.image.load("Images/pauseButton.png").convert_alpha()
pauseButtonImage = pygame.transform.scale(pauseButtonImage, (50, 50))
pauseButtonRect = pygame.rect.Rect(cg.SCREEN_WIDTH-50, 0, 50, 50)

resetButtonRect = pygame.rect.Rect(cg.SCREEN_WIDTH/2-50, 0, 100, 20)

def calculateSpeedFromSlider():
    startPos = cg.SCREEN_WIDTH - (speedSliderLength + 54)
    percentage = ((speedSliderPos[0] - startPos) / speedSliderLength) * 100
    speed = cg.minSpeed + (percentage / 100) * (cg.maxSpeed - cg.minSpeed)
    
    return speed

def drawPlayButton():
    cg.screen.blit(playButtonImage, playButtonRect)
    
def drawPauseButton():
    cg.screen.blit(pauseButtonImage, pauseButtonRect)
    
def drawSpeedSlider():
    global speedSliderPos
    
    if not speedSliderPos:
        speedSliderPos = [cg.SCREEN_WIDTH-(speedSliderLength/2)-54, speedSliderKnobRadius+1]
        
    sliderRect = pygame.rect.Rect(cg.SCREEN_WIDTH-speedSliderLength-54, (speedSliderKnobRadius+1)-10, speedSliderLength, 20)
    pygame.draw.rect(cg.screen, BLACK, sliderRect)
    
    pygame.draw.circle(cg.screen, LIGHT_BLUE, speedSliderPos, speedSliderKnobRadius)

def drawFpsCounter():
    if cg.currentFPS:
        currentFPS = str(cg.currentFPS)
    else:
        currentFPS = "-"
        
    currentFpsLabel = fpsLabelFont.render(f"FPS: {currentFPS}", True, BLACK)
    cg.screen.blit(currentFpsLabel, (0, 0))
    
    targetFpsLabel = fpsLabelFont.render(f"Target FPS: {cg.targetFPS}", True, BLACK)
    cg.screen.blit(targetFpsLabel, (0, currentFpsLabel.get_height()+5))

def drawResetButton():
    resetText = resetLabelFont.render("RESET", True, BLACK)
    
    pygame.draw.rect(cg.screen, BLACK, resetButtonRect, 2)
    cg.screen.blit(resetText, (cg.SCREEN_WIDTH/2-26, 2))

def adjustSpeedSlider(mousePos):
    global speedSliderPos
    
    mouseXpos = mousePos[0]
    
    if mouseXpos < cg.SCREEN_WIDTH-speedSliderLength-54 or mouseXpos > cg.SCREEN_WIDTH-54:
        return
    
    speedSliderPos[0] = mouseXpos
    cg.speed = calculateSpeedFromSlider()

def mouseDown(mousePos):
    if cg.paused:
        if playButtonRect.collidepoint(mousePos):
            cg.paused = False
            return True
    else:
        if pauseButtonRect.collidepoint(mousePos):
            cg.paused = True
            return True
    
    if not cg.usingSpeedSlider:
        distance = math.sqrt((mousePos[0] - speedSliderPos[0]) ** 2 + (mousePos[1] - speedSliderPos[1]) ** 2)
        
        if distance <= speedSliderKnobRadius:
            cg.usingSpeedSlider = True
            return True
        
    if resetButtonRect.collidepoint(mousePos):
        cg.reset = True
        return True
    
    return False
            
def drawDefaultInputGuis():
    if cg.paused:
        drawPlayButton()
    else:
        drawPauseButton()
        
    drawSpeedSlider()
    drawFpsCounter()
    drawResetButton()