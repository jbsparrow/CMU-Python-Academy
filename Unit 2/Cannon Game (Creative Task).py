class app:
    pass

app.background = 'skyBlue'
app.step = 0
app.startStep = 0
app.endStep = 0
app.slideInc = 6
app.allowMove = True
app.powerSlide = False
app.firing = False
app.firingStep = 0

# Oval(55,360,15,26,fill='black')
# Oval(70,360,15,26,fill='black')
cannon = Group(
Rect(30,350,40,20,fill='darkSlateGray'),
Arc(30,360,25,20,180,180,fill='darkSlateGray') # Back of arc coordinates: 20,360
)
cannon.step = 0

Rect(0,400,50,20,align='bottom-left',fill='saddleBrown')
Arc(25,380,25,25,-90,180,fill='sienna')
Polygon(0,380,0,320,50,380,fill='saddleBrown')

Rect(9,251,22,222,align='bottom-left') # Border was slightly uneven so this works better
powerBar = Rect(10,250,20,220,align='bottom-left',fill=gradient('red','yellow','green',start='bottom'))
powerSlider = Line(5,250,35,250,visible=False)

# -72.24737361476635
# 9.19365166790858

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
        fix = False
        if cannon.step < 5:
            cannon.children[0].width += 2
            cannon.children[0].height -= 2
        if cannon.step >= 5 and cannon.step < 8:
            cannon.children[0].width -= 1.666
            cannon.children[0].height += 1.666
            fix = True
        if fix:
            cannon.children[0].width = 40
            cannon.children[0].height = 20
        
        cannon.step += 1
        # print(cannon.step)
        
            
        







