# Import 
from Engine import *
import time
import random
from Perceptron import Perceptron

# Settings
rocketW = 1
W = 30
H = 30

# Output init
Output.resize(W, H)
Output.init()

# Input init
Input.init(extended=True)

# Object initialitaion
nn = Perceptron(3, 0.01)
window = Window(W,H)
ball = [random.randint(0, W-1), 0]
balls = [[random.randint(0, W-1), 0],[random.randint(0, W-1), 0]]
racket = [int(W/3), H - 1]

# Sys vars
y = 0
score = 0
force = False
enterPrevState = False
escPrevState = False

# Main loop
while True:
    if not force:
        time.sleep(0.1)
        Output.title(str(score))
    
    Input.tick()
    
    if Input.eventType == Input.Types.Keyboard:
        if Input.keyboardCode == Input.Keyboard.Keys.SPACE:
            force = Input.keyboardState == Input.Keyboard.DOWN

        if Input.keyboardCode == Input.Keyboard.Keys.ENTER:
            if Input.keyboardState == Input.Keyboard.DOWN:
                if enterPrevState != True:
                    file = open("nn.w", "w")
                    out = ""
                    for w in nn.w:
                        out += str(w) + "\n"
                    file.write(out)
                    file.close()
            enterPrevState = (Input.keyboardState == Input.Keyboard.DOWN)
                
        if Input.keyboardCode == Input.Keyboard.Keys.ESC:
            if Input.keyboardState == Input.Keyboard.DOWN:
                if escPrevState != True:
                    weights = open("nn.w", "r").read().split("\n")
                    for i in range(len(nn.w)):
                        nn.w[i] = float(weights[i])
            escPrevState = Input.keyboardState == Input.Keyboard.DOWN
    
    res = nn.predict([balls[0][0] / W, balls[0][1] / H, racket[0] / W])
    
    prevRacket = racket
    if res > 0.5:
        if racket[0] + rocketW < W:
            racket[0] += 1
        
    else:
        if racket[0] > 0:
            racket[0] += -1
    
    y += 1
    balls[0][1] += y % 2
    balls[1][1] += y % 2

    if balls[0][1] == racket[1]:
        balls[0][1] = 0
        
        if racket[0] <= balls[0][0] <= racket[0] + rocketW:
            score += 1
        else:
            if racket[0] + rocketW < balls[0][0]:
                nn.learnNoLearer(1)
                
            elif racket[0] > balls[0][0]:
                nn.learnNoLearer(-1)
        
        balls[1][1] = H // 2
        balls[0][0] = balls[1][0]
        balls[0][1] = balls[1][1]
        balls[1] = [random.randint(0, W-1), 0]

    if not force:
        window.fill()
        window.point(balls[0][0], balls[0][1])
        window.point(balls[1][0], balls[1][1])

        window.rect(racket[0], racket[1], rocketW, 1)
        window.draw()