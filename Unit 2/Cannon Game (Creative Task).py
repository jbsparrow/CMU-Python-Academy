app.background = 'skyBlue'
app.step = 0
app.startStep = 0
app.endStep = 0
# app.stepsPerSecond = 30
app.slideInc = 6
app.allowMove = True
app.powerSlide = False
app.firing = False
app.firingStep = 0
app.firingPower = 0
app.gravity = True
app.gravityForce = 9.81 # m/s^



app.pew = Sound('https://cdn.script-ware.net/pew.mp3')

# Oval(55,360,15,26,fill='black')
# Oval(70,360,15,26,fill='black')
cannon = Group(
Rect(30,350,40,20,fill='darkSlateGray'),
Arc(30,360,25,20,180,180,fill='darkSlateGray'), # Back of arc coordinates: 20,360
Circle(70,360,1,fill=None)
)
cannonball = Circle(cannon.children[2].centerX,cannon.children[2].centerY,5,fill='black')
cannonball.visible = False
cannonball.mass = 5 # kg
cannon.step = 0

Rect(0,400,50,20,align='bottom-left',fill='saddleBrown')
Arc(25,380,25,25,-90,180,fill='sienna')
Polygon(0,380,0,320,50,380,fill='saddleBrown')

Rect(9,251,22,222,align='bottom-left') # Border was slightly uneven so this works better
powerBar = Rect(10,250,20,220,align='bottom-left',fill=gradient('red','yellow','green',start='bottom'))
powerSlider = Line(5,250,35,250,visible=False)

# -72.24737361476635
# 9.19365166790858

def mapToRange(value:float, leftMin:float, leftMax:float, rightMin:float, rightMax:float) -> float:
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = (value - leftMin) / leftSpan

    return rightMin + (valueScaled * rightSpan)

def onMouseMove(mouseX,mouseY):
    cannonCenterY = (cannon.bottom - cannon.top) / 2 + cannon.top
    cannonRearX = cannon.left
    
    angleToMouse = angleTo(cannonRearX, cannonCenterY, mouseX, mouseY)
    angleToMouse -= 90
    if angleToMouse > -72 and angleToMouse < 9 and app.allowMove:
        cannon.rotateAngle = angleToMouse

def onMousePress(mouseX,mouseY):
    if not app.firing:
        if not app.powerSlide:
            app.allowMove = False
            powerSlider.y1 = powerBar.bottom
            powerSlider.y2 = powerBar.bottom
            app.slideInc = abs(app.slideInc)
            powerSlider.visible=True
            app.powerSlide = True
        elif app.powerSlide:
            app.powerSlide = False
            app.firing = True
            cannon.step = 0
            # Oval(cannon.children[2].centerX,cannon.children[2].centerY,)
            app.firingPower = powerSlider.y1 - powerBar.bottom
            print(app.firingPower)
            app.firingStep = 0
            # powerSlider.visible=False
            
            cannonball.centerX = cannon.children[2].centerX
            cannonball.centerY = cannon.children[2].centerY
            cannonball.step = 0
            multiplier = mapToRange(abs(powerSlider.y1 - powerBar.bottom), 0, 250, 0, 10)
            print(f'multiplier: {multiplier}')
            cannonball.xSpeed = dcos(cannon.rotateAngle) * multiplier
            cannonball.ySpeed = dsin(cannon.rotateAngle) * multiplier
            app.pew.play(restart=True)
            cannonball.visible = True
            print(cannonball.xSpeed, cannonball.ySpeed)
            


def onStep():
    app.step += 1
    if app.powerSlide: # Bounce the slider up and down
        powerSlider.y1 -= app.slideInc
        powerSlider.y2 -= app.slideInc
        if powerSlider.y1 <= powerBar.top:
            app.slideInc = -app.slideInc
        elif powerSlider.y1 >= powerBar.bottom:
            app.slideInc = abs(app.slideInc)
    if app.firing:
        cannonball.centerX += cannonball.xSpeed
        cannonball.centerY += cannonball.ySpeed
        # app.firing = False
    
    

