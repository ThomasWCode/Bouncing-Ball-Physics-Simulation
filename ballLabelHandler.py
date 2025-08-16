import pygame
pygame.init()

import globalConfig as cg

#COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

smallInfoFont = pygame.font.Font(None, 15)
largeInfoFont = pygame.font.Font(None, 32)

def getWidestTextSurface(texts):
    maxWidth = 0

    for text in texts:
        width = text.get_width()
        
        if width > maxWidth:
            maxWidth = width

    return maxWidth

class BallLabel:
    def __init__(self, ballInfo):    
        ballPos = (round(ballInfo['Pos'][0], 1), round(ballInfo['Pos'][1], 1))
        ballRadius = round(ballInfo['Radius'], 1)
        ballVel = (round(ballInfo['Vel'][0], 1), round(ballInfo['Vel'][1], 1))
        ballMass = round(ballInfo['Mass'], 1)
        ballVolume = round(ballInfo['Volume'], 1)
        
        text = f"Click ball for precise mesurements_Pos: {ballPos}_Radius: {ballRadius}_Velocity: {ballVel}_Mass: {ballMass}_Volume: {ballVolume}"
        
        labelTexts = []
        for text in text.split("_"):
            labelText = smallInfoFont.render(text, True, BLACK)
            labelTexts.append(labelText)
        
        frameHeight = len(labelTexts)*labelTexts[0].get_height()
        frameWidth = getWidestTextSurface(labelTexts)
        
        self.frameRect = pygame.rect.Rect(ballInfo["Pos"][0], ballInfo["Pos"][1], frameWidth, frameHeight)
        pygame.draw.rect(cg.screen, WHITE, self.frameRect)
        
        for i, labelText in enumerate(labelTexts):
            cg.screen.blit(labelText, (self.frameRect.left, self.frameRect.top+(i*labelText.get_height())))
            
class BallInfoBox:
    def __init__(self, ballInfo):
        ballPos = (ballInfo['Pos'][0], ballInfo['Pos'][1])
        ballRadius = ballInfo['Radius']
        ballVel = (ballInfo['Vel'][0], ballInfo['Vel'][1])
        ballMass = ballInfo['Mass']
        ballVolume = ballInfo['Volume']
        
        text = f"Pos: {ballPos}_Radius: {ballRadius}_Velocity: {ballVel}_Mass: {ballMass}_Volume: {ballVolume}"
        
        labelTexts = []
        for text in text.split("_"):
            labelText = largeInfoFont.render(text, True, BLACK)
            labelTexts.append(labelText)
        
        frameHeight = len(labelTexts)*labelTexts[0].get_height()
        frameWidth = getWidestTextSurface(labelTexts)
        
        self.frameRect = pygame.rect.Rect((cg.SCREEN_WIDTH/2)-(frameWidth/2), (cg.SCREEN_HEIGHT/2)-(frameHeight/2), frameWidth, frameHeight)
        pygame.draw.rect(cg.screen, WHITE, self.frameRect)
        
        for i, labelText in enumerate(labelTexts):
            cg.screen.blit(labelText, (self.frameRect.left, self.frameRect.top+(i*labelText.get_height())))
    
    def checkForClickOfInfoBox(self, mousePos):
        if not self.frameRect.collidepoint(mousePos):
            cg.showingBallInfoBox = [None, None]