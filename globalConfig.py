SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = None

#VARS
gravity = None
friction = None

reset = False

speed = 10
maxSpeed = 50
minSpeed = 0

currentFPS = None
targetFPS = None

balls = []
ballNum = None
ballRadius = None
ballColour = None
randomBallColours = False
showingBallInfoBox = [None, None]

paused = False

usingSpeedSlider = False

def resetAll():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, gravity, friction, reset, speed, maxSpeed, minSpeed, currentFPS, targetFPS, balls, ballNum, ballRadius, ballColour, randomBallColours, showingBallInfoBox, paused, usingSpeedSlider
    
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = None

    #VARS
    gravity = None
    friction = None
    
    reset = False

    speed = 10
    maxSpeed = 50
    minSpeed = 0

    currentFPS = None
    targetFPS = None

    balls = []
    ballNum = None
    ballRadius = None
    ballColour = None
    randomBallColours = False
    showingBallInfoBox = [None, None]

    paused = False

    usingSpeedSlider = False