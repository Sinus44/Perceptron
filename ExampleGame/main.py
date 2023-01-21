from Engine import *
import time
import random

W = 50
H = 30

Output.resize(W, H)
Output.init()
Input.init(extended = True)

nn = Perceptron(3, 0.01)
window = Window(W,H)

ball = [random.randint(0, W-1), 0]
racket = [int(W/3), H - 1]

rocketW = 1
y=0
score = 0
force = False

enterPrevState = False
escPrevState = False
while True:
    Input.tick()
    for event in Input.getEvents():
        if event.type == Input.Types.Keyboard:
            if event.keyboardCode == Input.Keyboard.Keys.SPACE:
                force = event.keyboardState == Input.Keyboard.DOWN
            if event.keyboardCode == Input.Keyboard.Keys.ENTER:
                if event.keyboardState == Input.Keyboard.DOWN:
                    if enterPrevState != True:
                        file = open("nn.w", "w")
                        out = ""
                        for w in nn.w:
                            out += str(w) + "\n"
                        file.write(out)
                        file.close()
                enterPrevState = (event.keyboardState == Input.Keyboard.DOWN)
                    
            if event.keyboardCode == Input.Keyboard.Keys.ESC:
                if event.keyboardState == Input.Keyboard.DOWN:
                    if escPrevState != True:
                        weights = open("nn.w", "r").read().split("\n")
                        for i in range(len(nn.w)):
                            nn.w[i] = float(weights[i])
                escPrevState = event.keyboardState == Input.Keyboard.DOWN
                  
    Output.title(str(score))
    if not force:
        time.sleep(0.1)
    
    window.fill(" ")
    window.point(ball[0], ball[1])
    
    res = nn.predict([ball[0] / W, ball[1] / H, racket[0] / W])
    
    prevRacket = racket
    if res > 0.5:
        if racket[0] + rocketW < W:
            racket[0] += 1
        
    elif res < 0.5:
        if racket[0] > 0:
            racket[0] += -1
    
    y += 1
    ball[1] += y%2
    
    if ball[1] == racket[1]:
        ball[1] = 0
        
        if racket[0] <= ball[0] <= racket[0] + rocketW:
            nn.learnNoLearer(0)
            score += 1
        else:
            if racket[0] + rocketW < ball[0]:
                nn.learnNoLearer(1)
                
            elif racket[0] > ball[0]:
                nn.learnNoLearer(-1)
                
        ball[0] = random.randint(0, W-1)
            
    window.rect(racket[0], racket[1], rocketW, 1)
    window.draw()