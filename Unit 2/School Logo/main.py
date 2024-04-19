import json
app.enable_imports = False


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
                line.lineWidth = app.lineWidth
            elif i >= current_lines and i < self.num_segments:
                new_line = Line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], lineWidth=app.lineWidth, fill='black', opacity=75)
                self.group.add(new_line)

        # Remove excess lines if the number of segments decreased
        while len(self.group.children) > self.num_segments:
            self.group.remove(self.group.children[-1])


class BezierPolygon:
    def __init__(self, segments_data, fill_color='gray', border_color='black'):
        """Initialize the polygon composed of multiple Bezier curves."""
        self.segments_data = segments_data
        self.fill_color = fill_color
        self.border_color = border_color
        self.polygon = None
        self.create_polygon()

    def create_polygon(self):
        """Create a polygon using points calculated from the Bezier curves."""
        all_points = []
        for control_points, num_segments in self.segments_data:
            num_segments = int(num_segments)
            points = [self.cubic_bezier(t / num_segments, *control_points) for t in range(num_segments + 1)]
            if all_points:  # Remove the last point to avoid duplicates between segments
                points = points[1:]
            all_points.extend(points)
        
        polygon_points = [[x, y] for x, y in all_points]
        self.polygon = Polygon(0,0)
        self.polygon.fill = self.fill_color
        self.polygon.border = self.border_color
        self.polygon.pointList = polygon_points

    def cubic_bezier(self, t, P0, P1, P2, P3):
        """Calculate the point on the cubic Bezier curve for a given parameter t."""
        x = (1 - t)**3 * P0[0] + 3 * (1 - t)**2 * t * P1[0] + 3 * (1 - t) * t**2 * P2[0] + t**3 * P3[0]
        y = (1 - t)**3 * P0[1] + 3 * (1 - t)**2 * t * P1[1] + 3 * (1 - t) * t**2 * P2[1] + t**3 * P3[1]
        return (x, y)


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
        label.value = str(value)
        label.fill = 'crimson'
    else:
        label.value = str(value)
        label.fill = 'forestGreen'
    label.toFront()

def changeStartPoint():
    if app.selectedStart == 1:
        updateSelectedPoint(app.selectedStartPoint, app.p0[0], app.p0[1])
        app.bzPoint = 1
    else:
        updateSelectedPoint(app.selectedStartPoint, app.p3[0], app.p3[1])
        app.bzPoint = 4

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

def importBezier(bezierType, bezierData: str):
    try:
        bezierList = json.loads(bezierData)
    except:
        print('Invalid input.')
        app.importingItems = False
        return

    if bezierType == 'line':
        startBezierIndex = len(app.bezierLines)
        endBezierIndex = startBezierIndex + len(bezierList)
        for i in bezierList:
            bezierLine = Bezier(i[0], i[1])
            app.bezierLines.append(bezierLine)
        return startBezierIndex, endBezierIndex

    elif bezierType == 'polygon':
        bezierPolygon = BezierPolygon(bezierList)
        bezierPolygon.polygon.toFront()
        return bezierPolygon


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
        app.lockedPoint = 1 if app.selectedStart == 4 else 4
        if app.selectedStart == 4:
            app.p0 = app.p3
            updateSelectedPoint(app.p0Label, app.p0[0], app.p0[1])
        else:
            app.p3 = app.p0
            updateSelectedPoint(app.p3Label, app.p3[0], app.p3[1])
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
            importBezier('line', input)
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

    if key == 'up':
        app.lineWidth += 1
        for i in app.bezierLines:
            for child in i.group.children:
                child.lineWidth = app.lineWidth
        return

    if key == 'down':
        if app.lineWidth > 1:
            app.lineWidth -= 1
            for i in app.bezierLines:
                for child in i.group.children:
                    child.lineWidth = app.lineWidth
        return


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
    elif key == '=':
        app.bezierPolygonalPoints += 1
        app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        app.polypoints.value = str(app.bezierPolygonalPoints)
    elif key == '-':
        if app.bezierPolygonalPoints > 1:
            app.bezierPolygonalPoints -= 1
            app.bezierLines[app.currentBezierIndex].update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
            app.polypoints.value = str(app.bezierPolygonalPoints)
    elif key == 'enter':
        parameterList = []
        for i in app.bezierLines:
            parameters = []
            parameters.append([list(v) for v in i.control_points])
            parameters.append(i.num_segments)
            parameterList.append(parameters)
        print(json.dumps(parameterList))
    elif key == '\\':
        pointList = []
        for i in app.bezierLines:
            for j in i.group.children:
                pointList.append([j.x1, j.y1])
        print(json.dumps(pointList))
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


def polyGen(points):
    poly = Polygon(0,0)
    poly.fill = 'black'
    poly.pointList = points
    return poly


app.enable_imports = True
if app.enable_imports:
    
    shieldOutlineStartIndex, shieldOutlineEndIndex = importBezier('line', '[[[[68, 88], [93, 51], [305, 48], [332, 88]], 20], [[[332, 88], [354, 230], [238, 343], [200, 368]], 20], [[[200, 368], [160, 339], [46, 233], [68, 88]], 20]]')
    for drawing in app.bezierLines[shieldOutlineStartIndex:shieldOutlineEndIndex]:
        for child in drawing.group.children:
            child.fill = 'black'
            child.lineWidth = 2
    
    
    J_outline = importBezier('polygon', '[[[[33, 214], [82, 76], [94, 200], [58, 223]], 1], [[[58, 223], [82, 76], [94, 200], [58, 302]], 1], [[[58, 302], [58, 310], [53, 317], [43, 318]], 15], [[[43, 318], [58, 310], [53, 317], [26, 317]], 1], [[[26, 317], [58, 310], [53, 317], [27, 289]], 1], [[[27, 289], [58, 310], [53, 317], [33, 291]], 1], [[[33, 291], [58, 310], [53, 317], [33, 214]], 1]]')
    J_outline.polygon.fill = 'black'

    J_line_startIndex, J_line_endIndex = importBezier('line', '[[[[37, 219], [82, 76], [94, 200], [54, 225]], 1], [[[54, 225], [82, 76], [94, 200], [54, 301]], 1], [[[54, 301], [53, 306], [51, 312], [44, 312]], 15], [[[44, 312], [53, 306], [51, 312], [30, 312]], 1], [[[30, 312], [53, 306], [51, 312], [31, 294]], 1], [[[31, 294], [36, 297], [37, 293], [37, 290]], 15], [[[37, 290], [36, 297], [39, 293], [37, 219]], 1]]')
    for drawing in app.bezierLines[J_line_startIndex:J_line_endIndex]:
        for child in drawing.group.children:
            child.fill = 'white'
            child.lineWidth = 2


    Jag_Outline = importBezier('polygon', '[[[[129, 69], [57, 102], [73, 189], [135, 223]], 25], [[[135, 223], [152, 199], [199, 209], [209, 219]], 10], [[[209, 219], [231, 256], [272, 237], [267, 212]], 10], [[[267, 212], [231, 256], [272, 237], [282, 186]], 1], [[[282, 186], [231, 256], [272, 237], [267, 191]], 1], [[[267, 191], [266, 180], [278, 163], [282, 165]], 15], [[[282, 165], [266, 180], [278, 163], [286, 177]], 1], [[[286, 177], [266, 180], [278, 163], [295, 161]], 1], [[[295, 161], [317, 155], [329, 137], [319, 117]], 15], [[[319, 117], [323, 112], [323, 110], [317, 105]], 15], [[[317, 105], [320, 100], [316, 94], [302, 81]], 15], [[[302, 81], [320, 100], [316, 94], [303, 73]], 1], [[[303, 73], [310, 75], [315, 54], [286, 54]], 15], [[[286, 54], [270, 38], [219, 12], [166, 39]], 15], [[[166, 39], [139, 42], [124, 31], [107, 17]], 15], [[[107, 17], [103, 37], [104, 59], [129, 69]], 15]]')
    Jag_Outline.polygon.fill = 'black'
    Jag_Outline.polygon.opacity = 30
    
    black_details = [
        '[[[[127, 82], [82, 76], [94, 200], [138, 85]], 1], [[[138, 85], [111, 104], [95, 122], [92, 149]], 8], [[[92, 149], [86, 117], [116, 90], [127, 82]], 9]]',
        '[[[[113, 115], [91, 149], [108, 198], [119, 211]], 10], [[[119, 211], [91, 149], [108, 198], [133, 221]], 1], [[[133, 221], [141, 208], [170, 197], [197, 205]], 15], [[[197, 205], [141, 208], [170, 197], [210, 218]], 1], [[[210, 218], [225, 250], [271, 246], [267, 211]], 15], [[[267, 211], [225, 250], [271, 246], [261, 214]], 1], [[[261, 214], [265, 233], [238, 246], [221, 224]], 15], [[[221, 224], [198, 198], [185, 175], [131, 184]], 15], [[[131, 184], [122, 167], [114, 145], [144, 107]], 15], [[[144, 107], [126, 114], [106, 157], [126, 190]], 15], [[[126, 190], [159, 179], [179, 192], [192, 201]], 15], [[[192, 201], [168, 195], [136, 207], [130, 217]], 15], [[[130, 217], [112, 197], [101, 163], [113, 115]], 15]]',
        '[[[[134, 222], [155, 202], [176, 205], [201, 210]], 15], [[[201, 210], [155, 202], [176, 205], [209, 218]], 1], [[[209, 218], [168, 200], [149, 211], [134, 222]], 15]]',
        '[[[[135, 222], [69, 183], [70, 102], [132, 70]], 20], [[[132, 70], [114, 57], [106, 47], [110, 26]], 20], [[[110, 26], [119, 51], [136, 54], [149, 57]], 20], [[[149, 57], [129, 49], [120, 40], [110, 27]], 20], [[[110, 27], [128, 37], [142, 45], [168, 43]], 15], [[[168, 43], [187, 24], [255, 25], [284, 54]], 15], [[[284, 54], [187, 24], [255, 25], [287, 54]], 1], [[[287, 54], [254, 24], [197, 20], [166, 39]], 15], [[[166, 39], [136, 40], [124, 32], [107, 18]], 15], [[[107, 18], [103, 40], [107, 59], [126, 70]], 15], [[[126, 70], [68, 98], [62, 179], [133, 222]], 15]]',
        '[[[[281, 54], [295, 49], [332, 70], [287, 74]], 15], [[[287, 74], [295, 49], [332, 70], [283, 80]], 1], [[[283, 80], [295, 49], [332, 70], [274, 73]], 1], [[[274, 73], [273, 73], [270, 74], [269, 75]], 1], [[[269, 75], [273, 73], [276, 65], [276, 61]], 15], [[[276, 61], [279, 64], [279, 67], [279, 71]], 15], [[[279, 71], [294, 75], [332, 59], [277, 57]], 15], [[[277, 57], [294, 75], [332, 59], [282, 54]], 1]]',
        '[[[[265, 98], [265, 105], [268, 109], [273, 112]], 15], [[[273, 112], [273, 116], [282, 121], [285, 119]], 15], [[[285, 119], [270, 111], [295, 108], [300, 132]], 15], [[[300, 132], [270, 111], [295, 108], [319, 116]], 1], [[[319, 116], [321, 115], [321, 108], [317, 105]], 15], [[[317, 105], [319, 101], [319, 95], [301, 82]], 15], [[[301, 82], [319, 101], [319, 95], [303, 73]], 1], [[[303, 73], [319, 101], [319, 95], [299, 76]], 1], [[[299, 76], [319, 101], [319, 95], [298, 83]], 1], [[[298, 83], [315, 98], [315, 99], [313, 104]], 15], [[[313, 104], [315, 98], [315, 99], [306, 100]], 1], [[[306, 100], [303, 94], [301, 92], [291, 83]], 15], [[[291, 83], [303, 94], [301, 92], [290, 85]], 1], [[[290, 85], [298, 91], [303, 99], [303, 100]], 15], [[[303, 100], [281, 95], [271, 119], [265, 98]], 15]]',
        '[[[[299, 71], [82, 76], [94, 200], [301, 75]], 1], [[[301, 75], [82, 76], [94, 200], [308, 69]], 1], [[[308, 69], [306, 66], [309, 64], [306, 65]], 1], [[[306, 65], [306, 66], [305, 69], [299, 71]], 15]]',
        '[[[[121, 117], [127, 100], [142, 91], [150, 88]], 15], [[[150, 88], [153, 110], [157, 118], [161, 123]], 15], [[[161, 123], [178, 118], [185, 110], [218, 109]], 15], [[[218, 109], [193, 113], [175, 121], [160, 131]], 15], [[[160, 131], [154, 119], [146, 100], [147, 95]], 15], [[[147, 95], [134, 99], [129, 109], [121, 117]], 15]]',
        '[[[[184, 96], [198, 88], [213, 85], [223, 90]], 15], [[[223, 90], [219, 92], [217, 94], [215, 97]], 15], [[[215, 97], [222, 95], [237, 92], [257, 99]], 15], [[[257, 99], [234, 96], [214, 97], [206, 104]], 15], [[[206, 104], [207, 95], [210, 96], [212, 92]], 15], [[[212, 92], [206, 92], [197, 92], [184, 96]], 15]]',
        
        ]
    for detail in black_details:
        d=importBezier('polygon', detail)
        d.polygon.fill = 'black'

    white_details = [
        '[[[[286, 121], [82, 76], [94, 200], [281, 125]], 1], [[[281, 125], [258, 120], [207, 126], [162, 137]], 15], [[[162, 137], [216, 120], [263, 117], [286, 121]], 15]]',
        '[[[[279, 127], [82, 76], [94, 200], [274, 131]], 1], [[[274, 131], [253, 130], [203, 131], [139, 148]], 6], [[[139, 148], [196, 130], [247, 125], [279, 127]], 7]]',
        '[[[[271, 135], [82, 76], [94, 200], [265, 138]], 1], [[[265, 138], [230, 134], [161, 146], [138, 153]], 15], [[[138, 153], [197, 134], [243, 131], [271, 135]], 15]]',
        
    ]
    for detail in white_details:
        d=importBezier('polygon', detail)
        d.polygon.fill = 'white'
        d.polygon.border = 'white'


def onStep():
    pass