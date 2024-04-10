import random
import math


app.background = 'skyBlue'
app.slideInc = 6 # Power slider increment
app.allowMove = True # Allow cannon movement
app.powerSlide = False # Is the power slider moving?
app.firing = False # Is the cannonball being fired?
app.firingPower = 0 # Firepower multiplier
app.gravity = True # Gravity toggle
app.gravityForce = 9.81 # m/s^2
app.singleSplat = False # Only allow one splat per cannonball
app.splats = [] # List of splats

app.pew = Sound('https://cdn.script-ware.net/pew.mp3')
app.splat = Sound('https://cdn.script-ware.net/splat.mp3')


# Cannon
cannon = Group(
Rect(30,350,40,20,fill='darkSlateGray'),
Arc(30,360,25,20,180,180,fill='darkSlateGray'), # Back of arc coordinates: 20,360
Circle(70,360,1,fill=None)
)
cannonball = Circle(cannon.children[2].centerX,cannon.children[2].centerY,5,fill='black')
cannonball.visible = False

# Cannon Base
Rect(0,400,50,20,align='bottom-left',fill='saddleBrown')
Arc(25,380,25,25,-90,180,fill='sienna')
Polygon(0,380,0,320,50,380,fill='saddleBrown')

# Shot Power Slider
Rect(9,251,22,222,align='bottom-left') # Border was slightly uneven so this works better
powerBar = Rect(10,250,20,220,align='bottom-left',fill=gradient('red','yellow','green',start='bottom'))
powerSlider = Line(5,250,35,250,visible=False)


def generateSplat(center_x:float, center_y:float, radius:float, num_ovals:int=6) -> Group:
    splat = Group(
    Circle(center_x, center_y, random.uniform(radius - (radius / 2), radius + radius),fill=None) # Draw center of splat
    )
    angle_step = 360 / num_ovals
    
    for i in range(num_ovals):
        base_angle = angle_step * i
        angle = base_angle + random.uniform(-10, 10)  # Randomize the angle
        
        # Randomize the size of ovals
        oval_width = random.uniform(10, 30)
        oval_height = random.uniform(25, 45)
        
        distance = radius + oval_height * 0.01
        oval_x = center_x + distance * math.cos(math.radians(angle))
        oval_y = center_y + distance * math.sin(math.radians(angle))
        
        oval = Oval(oval_x, oval_y, oval_width, oval_height)
        
        # Rotate the oval
        oval.rotateAngle = angle+90
        splat.add(oval)
    
    return splat


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
            
            cannonball.centerX = cannon.children[2].centerX
            cannonball.centerY = cannon.children[2].centerY
            app.firingPower = mapToRange(abs(powerSlider.y1 - powerBar.bottom), 0, 250, 0, 20)
            cannonball.xSpeed = dcos(cannon.rotateAngle) * app.firingPower
            cannonball.ySpeed = dsin(cannon.rotateAngle) * app.firingPower
            app.pew.play(restart=True)
            cannonball.visible = True
            app.singleSplat = False


def onStep():
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
        
        if app.gravity:
            cannonball.ySpeed += app.gravityForce * (1/app.stepsPerSecond)
        
        if cannonball.right >= 400 or cannonball.bottom >= 400 or cannonball.top <= 0:
            if not app.singleSplat:
                paint_splat = generateSplat(200, 200, random.uniform(11,16), num_ovals=int(random.uniform(6,8)))
                paint_splat.centerX = cannonball.centerX
                paint_splat.centerY = cannonball.centerY
                if paint_splat.bottom > 400:
                    paint_splat.bottom = 400
                if paint_splat.right > 400:
                    paint_splat.right = 400
                if paint_splat.top < 0:
                    paint_splat.top = 0
                for s in [i for i in app.splats if i.opacity > 0]:
                        s.opacity -= 25
                app.splats.append(paint_splat)
                app.splat.play(restart=True)
                app.singleSplat = True
        
        if cannonball.centerX > 425 or cannonball.centerX < -20 or cannonball.centerY > 425 or cannonball.centerY < -20:
            cannonball.visible = False
            app.firing = False
            powerSlider.visible = False
            app.allowMove = True

