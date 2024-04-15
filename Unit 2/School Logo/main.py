import json


jag = Image('https://cdn.script-ware.net/jag.jpg', 200, 200, opacity=50, align='center')
jag.width = 390
jag.height = 366
jag.centerX = 200
jag.centerY = 200

app.lineWidth = 1


class Bezier:
    def __init__(self, control_points, num_segments):
        """Initialize the Bezier curve with control points and a specific number of segments."""
        self.control_points = control_points
        self.num_segments = num_segments
        self.group = self.create_bezier_group()

    def cubic_bezier(self, t, P0, P1, P2, P3):
        """Calculate the point on the cubic Bezier curve for a given parameter t."""
        x = (1 - t)**3 * P0[0] + 3 * (1 - t)**2 * t * P1[0] + 3 * (1 - t) * t**2 * P2[0] + t**3 * P3[0]
        y = (1 - t)**3 * P0[1] + 3 * (1 - t)**2 * t * P1[1] + 3 * (1 - t) * t**2 * P2[1] + t**3 * P3[1]
        return (x, y)

    def create_bezier_group(self):
        """Create a group of line segments to represent the Bezier curve."""
        P0, P1, P2, P3 = self.control_points
        points = [self.cubic_bezier(t / self.num_segments, P0, P1, P2, P3) for t in range(self.num_segments + 1)]
        group = Group()
        for i in range(len(points) - 1):
            line = Line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], lineWidth=app.lineWidth, fill='black', opacity=75)
            group.add(line)
        return group

    def update(self, control_points=None, num_segments=None):
        """Update the Bezier curve with new control points or a different number of segments."""
        if control_points:
            self.control_points = control_points
        if num_segments is not None:
            self.num_segments = num_segments

        points = [self.cubic_bezier(t / self.num_segments, *self.control_points) for t in range(self.num_segments + 1)]
        current_lines = len(self.group.children)

        # Update existing lines or add new ones if necessary
        for i in range(max(current_lines, self.num_segments)):
            if i < current_lines and i < self.num_segments:
                line = self.group.children[i]
                line.x1 = points[i][0]
                line.y1 = points[i][1]
                line.x2 = points[i + 1][0]
                line.y2 = points[i + 1][1]
            elif i >= current_lines and i < self.num_segments:
                new_line = Line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], lineWidth=app.lineWidth, fill='black', opacity=75)
                self.group.add(new_line)

        # Remove excess lines if the number of segments decreased
        while len(self.group.children) > self.num_segments:
            self.group.remove(self.group.children[-1])


def Point(x,y):
    return (x,y)


app.bzPoint = 0 # Control point selected
app.p0 = Point(67,87)
app.p1 = Point(82,76)
app.p2 = Point(94,200)
app.p3 = Point(121,65)
app.bezierPolygonalPoints = 15 # Number of points to draw the bezier curve
app.polypoints = Label(str(app.bezierPolygonalPoints), 20, 20, size=12, fill='black')
app.selectedPoint = Label(str(app.bzPoint) if app.bzPoint != 0 else 'N', 40,20,size=12,fill='crimson')
app.p0Label = Label('1', app.p0[0], app.p0[1], size=15, fill='crimson')
app.p1Label = Label('2', app.p1[0], app.p1[1], size=15, fill='crimson')
app.p2Label = Label('3', app.p2[0], app.p2[1], size=15, fill='crimson')
app.p3Label = Label('4', app.p3[0], app.p3[1], size=15, fill='crimson')
app.importingItems = False


# Seamless Bezier Sketching Variables
app.bezierLines = [Bezier([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)]
app.currentBezierIndex = 0
app.switchingBezier = False
app.savedPoint = Point(200,200)
app.selectingNewStart = False
app.selectedStart = 0 # 1 or 4 - Where to start the new bezier line
app.lockedPoint = 0 # Used to lock the start point of the bezier line
app.finalPoint = 0 # Used to bridge the last bezier line with the first one


app.selectedStartPoint = Circle(app.p0[0], app.p0[1], 5, fill=None, border='black', borderWidth=1, visible=False)
app.selectedStartPoint.toBack()
app.bezierLines[app.currentBezierIndex].group.toFront()
app.p0Label.toFront()
app.p1Label.toFront()
app.p2Label.toFront()
app.p3Label.toFront()


def updateSelectedPoint(point, x, y):
    point.centerX = x
    point.centerY = y
    point.toFront()
    app.p0Label.toFront()
    app.p1Label.toFront()
    app.p2Label.toFront()
    app.p3Label.toFront()

def updateCurrentVerticeLabel(label, value):
    if value == 0:
        label.value = 'N'
        label.fill = 'crimson'
    elif value == app.lockedPoint:
        label.value = str(app.selectedPoint)
        label.fill = 'crimson'
    else:
        label.value = str(value)
        label.fill = 'forestGreen'
    label.toFront()

def changeStartPoint():
    if app.selectedStart == 1:
        updateSelectedPoint(app.selectedStartPoint, app.p0[0], app.p0[1])
        app.bzPoint = 4
    else:
        updateSelectedPoint(app.selectedStartPoint, app.p3[0], app.p3[1])
        app.bzPoint = 1

    if app.selectingNewStart:
        app.selectedStartPoint.visible = True
    else:
        app.selectedStartPoint.visible = False

    if app.finalPoint == 0:
        app.finalPoint = app.selectedStart

def switchCurrentBezier():
    app.p0, app.p1, app.p2, app.p3 = app.bezierLines[app.currentBezierIndex].control_points
    app.bezierPolygonalPoints = app.bezierLines[app.currentBezierIndex].num_segments
    app.bezierLines[app.currentBezierIndex].group.toFront()
    updateSelectedPoint(app.p0Label, app.p0[0], app.p0[1])
    updateSelectedPoint(app.p1Label, app.p1[0], app.p1[1])
    updateSelectedPoint(app.p2Label, app.p2[0], app.p2[1])
    updateSelectedPoint(app.p3Label, app.p3[0], app.p3[1])
    app.polypoints.value = str(app.bezierPolygonalPoints)


def onKeyPress(key):
    if key == 'space' and not app.switchingBezier:
        app.selectingNewStart = not app.selectingNewStart
        if app.selectingNewStart:
            if app.p0[0] > app.p3[0]:
                app.selectedStart = 4
            else:
                app.selectedStart = 1
            changeStartPoint()
            return
        else:
            app.selectedStartPoint.visible = False
            app.selectedStart = 0
            return

    if app.selectingNewStart and key == 'left' and not app.switchingBezier:
        if app.selectedStart == 1:
            app.selectedStart = 4
        else:
            app.selectedStart = 1
        changeStartPoint()
        return

    if app.selectingNewStart and key == 'right' and not app.switchingBezier:
        if app.selectedStart == 1:
            app.selectedStart = 4
        else:
            app.selectedStart = 1
        changeStartPoint() 
        return

    if app.selectingNewStart and key == 'enter' and not app.switchingBezier:
        app.selectingNewStart = False
        app.selectedStartPoint.visible = False
        app.bezierLines.append(Bezier([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints))
        app.currentBezierIndex += 1
        app.lockedPoint = app.selectedStart
        app.bezierLines[app.currentBezierIndex].group.toFront()
        updateCurrentVerticeLabel(app.selectedPoint, app.bzPoint)
        return


    if key == '[':
        if app.bzPoint != 0:
            app.savedPoint = app.bezierLines[app.currentBezierIndex].control_points[app.bzPoint - 1]
        return

    if key == ']':
        if app.bzPoint == 1:
            app.p0 = app.savedPoint
            updateSelectedPoint(app.p0Label, app.p0[0], app.p0[1])
        elif app.bzPoint == 2:
            app.p1 = app.savedPoint
            updateSelectedPoint(app.p1Label, app.p1[0], app.p1[1])
        elif app.bzPoint == 3:
            app.p2 = app.savedPoint
            updateSelectedPoint(app.p2Label, app.p2[0], app.p2[1])
        elif app.bzPoint == 4:
            app.p3 = app.savedPoint
            updateSelectedPoint(app.p3Label, app.p3[0], app.p3[1])
        app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)


    if key == 'x':
        app.switchingBezier = not app.switchingBezier
        return

    if app.switchingBezier and key == 'left':
        if app.currentBezierIndex > 0:
            app.currentBezierIndex -= 1
        elif app.currentBezierIndex == 0:
            app.currentBezierIndex = len(app.bezierLines) - 1
        switchCurrentBezier()
        return

    if app.switchingBezier and key == 'right':
        if app.currentBezierIndex < len(app.bezierLines) - 1:
            app.currentBezierIndex += 1
        elif app.currentBezierIndex == len(app.bezierLines) - 1:
            app.currentBezierIndex = 0
        switchCurrentBezier()
        return


    if key == 'backspace' and not app.switchingBezier and not app.selectingNewStart and not app.importingItems:
        # Remove the currently selected bezierLine
        if len(app.bezierLines) > 1:
            app.bezierLines[app.currentBezierIndex].group.clear()
            app.bezierLines.pop(app.currentBezierIndex)
            if app.currentBezierIndex == len(app.bezierLines):
                app.currentBezierIndex -= 1
            switchCurrentBezier()
            return


    if key == 'i' and not app.importingItems:
        app.importingItems = True
        try:
            input = app.getTextInput('Paste bezier JSON string here.')
            try:
                bezierList = json.loads(input)
                for i in bezierList:
                    app.bezierLines.append(Bezier(i["Control Points"], i["Number of Segments"]))
                app.importingItems = False
            except:
                print('Invalid input.')
                app.importingItems = False
        except:
            app.importingItems = False
            return

    # Adjust coordinates of the currently selected point
    if key == 'e':
        if app.bzPoint == 0 or app.bzPoint == app.lockedPoint:
            pass
        try:
            print(f'\n\n\n\n\n\n\n\n\nPoint 1: {tuple(app.p0)}')
            print(f'Point 2: {tuple(app.p1)}')
            print(f'Point 3: {tuple(app.p2)}')
            print(f'Point 4: {tuple(app.p3)}')
            
            
            x = app.getTextInput(f'Adjust x value for point {app.bzPoint} (current: {app.bezierLines[app.currentBezierIndex].control_points[app.bzPoint - 1][0]})')
            if x == '':
                x = app.bezierLines[app.currentBezierIndex].control_points[app.bzPoint - 1][0]
            y = app.getTextInput(f'y coordinate (current: {app.bezierLines[app.currentBezierIndex].control_points[app.bzPoint - 1][1]})')
            if y == '':
                y = app.bezierLines[app.currentBezierIndex].control_points[app.bzPoint - 1][1]
            if app.bzPoint == 1:
                updateSelectedPoint(app.p0Label, int(x), int(y))
                app.p0 = Point(int(x), int(y))
            elif app.bzPoint == 2:
                updateSelectedPoint(app.p1Label, int(x), int(y))
                app.p1 = Point(int(x), int(y))
            elif app.bzPoint == 3:
                updateSelectedPoint(app.p2Label, int(x), int(y))
                app.p2 = Point(int(x), int(y))
            elif app.bzPoint == 4:
                updateSelectedPoint(app.p3Label, int(x), int(y))
                app.p3 = Point(int(x), int(y))
            app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        except Exception as e:
            print('Invalid input.')
            print(e)
        return

    # Mirror the last bezier line across the y-axis
    if key == 'm':
        app.p0 = Point(400 - app.p0[0], app.p0[1])
        app.p1 = Point(400 - app.p1[0], app.p1[1])
        app.p2 = Point(400 - app.p2[0], app.p2[1])
        app.p3 = Point(400 - app.p3[0], app.p3[1])
        app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        updateSelectedPoint(app.p0Label, app.p0[0], app.p0[1])
        updateSelectedPoint(app.p1Label, app.p1[0], app.p1[1])
        updateSelectedPoint(app.p2Label, app.p2[0], app.p2[1])
        updateSelectedPoint(app.p3Label, app.p3[0], app.p3[1])
        return

    # Mirror the last bezier line across the x-axis
    if key == 'y':
        app.p0 = Point(app.p0[0], 400 - app.p0[1])
        app.p1 = Point(app.p1[0], 400 - app.p1[1])
        app.p2 = Point(app.p2[0], 400 - app.p2[1])
        app.p3 = Point(app.p3[0], 400 - app.p3[1])
        app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        updateSelectedPoint(app.p0Label, app.p0[0], app.p0[1])
        updateSelectedPoint(app.p1Label, app.p1[0], app.p1[1])
        updateSelectedPoint(app.p2Label, app.p2[0], app.p2[1])
        updateSelectedPoint(app.p3Label, app.p3[0], app.p3[1])
        return

    if key == 's':
        app.bezierPolygonalPoints =1
        app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        app.polypoints.value = str(app.bezierPolygonalPoints)
        return


    if key == 'n':
        app.bezierPolygonalPoints = 15
        app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        app.polypoints.value = str(app.bezierPolygonalPoints)
        return

    if key == 'h':
        app.p0Label.visible = not app.p0Label.visible
        app.p1Label.visible = not app.p1Label.visible
        app.p2Label.visible = not app.p2Label.visible
        app.p3Label.visible = not app.p3Label.visible


    if key == '0':
        app.bzPoint = 0
        updateCurrentVerticeLabel(app.selectedPoint, app.bzPoint)
    elif key == '1':
        app.bzPoint = 1
        updateCurrentVerticeLabel(app.selectedPoint, app.bzPoint)
    elif key == '2':
        app.bzPoint = 2
        updateCurrentVerticeLabel(app.selectedPoint, app.bzPoint)
    elif key == '3':
        app.bzPoint = 3
        updateCurrentVerticeLabel(app.selectedPoint, app.bzPoint)
    elif key == '4':
        app.bzPoint = 4
        updateCurrentVerticeLabel(app.selectedPoint, app.bzPoint)
    elif key == 'up' or key == '=':
        app.bezierPolygonalPoints += 1
        app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        app.polypoints.value = str(app.bezierPolygonalPoints)
    elif key == 'down' or key == '-':
        if app.bezierPolygonalPoints > 1:
            app.bezierPolygonalPoints -= 1
            app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
            app.polypoints.value = str(app.bezierPolygonalPoints)
    elif key == 'enter':
        parameterList = []
        for i in app.bezierLines:
            parameters = {"Control Points": [list(v) for v in i.control_points], "Number of Segments": i.num_segments}
            parameterList.append(parameters)
        print(json.dumps(parameterList))
    elif key == 't':
        if app.lockedPoint == 1:
            app.p3 = app.bezierLines[0].control_points[3]
            app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
            updateSelectedPoint(app.p3Label, app.p3[0], app.p3[1])
        elif app.lockedPoint == 4:
            app.p0 = app.bezierLines[0].control_points[0]
            app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
            updateSelectedPoint(app.p0Label, app.p0[0], app.p0[1])

def onMouseDrag(x, y):
    if app.bzPoint == 1 and app.lockedPoint != 1:
        app.p0 = Point(x, y)
        updateSelectedPoint(app.p0Label, x, y)
    elif app.bzPoint == 2:
        app.p1 = Point(x, y)
        updateSelectedPoint(app.p1Label, x, y)
    elif app.bzPoint == 3:
        app.p2 = Point(x, y)
        updateSelectedPoint(app.p2Label, x, y)
    elif app.bzPoint == 4 and app.lockedPoint != 4:
        app.p3 = Point(x, y)
        updateSelectedPoint(app.p3Label, x, y)
    app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)



def onStep():
    pass