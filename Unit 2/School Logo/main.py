jag = Image('https://cdn.script-ware.net/jag.jpg', 200, 200, opacity=50, align='center')
jag.width = 390
jag.height = 366
jag.centerX = 200
jag.centerY = 200


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
            line = Line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
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
                new_line = Line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
                self.group.add(new_line)

        # Remove excess lines if the number of segments decreased
        while len(self.group.children) > self.num_segments:
            self.group.remove(self.group.children[-1])



def Point(x,y):
    return [x,y]


app.bzPoint = 0
app.p0 = Point(67,87)
app.p1 = Point(82,76)
app.p2 = Point(94,200)
app.p3 = Point(121,65)
app.bezierPolygonalPoints = 15
app.polypoints = Label(str(app.bezierPolygonalPoints), 20, 20, size=12, fill='black')
app.selectedPoint = Label(str(app.bzPoint) if app.bzPoint != 0 else 'N', 40,20,size=12,fill='crimson')
app.p0Label = Label('1', app.p0[0], app.p0[1], size=12, fill='crimson')
app.p1Label = Label('2', app.p1[0], app.p1[1], size=12, fill='crimson')
app.p2Label = Label('3', app.p2[0], app.p2[1], size=12, fill='crimson')
app.p3Label = Label('4', app.p3[0], app.p3[1], size=12, fill='crimson')

# app.bezier = Bezier([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)


app.bezierLine = Bezier([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
app.bezierLines = []
app.selectingNewStart = False
app.selectedStart = 0
app.lockedPoint = 0


polyOpacity = 100
# Polygon(200,370,178,352,162,336,82,215,77,203,68,169,65,149,64,123,65,96,67,87,70,84,82,76,94,71,110,66,121,65,    306,71,307,72,318,76,330,84,333,87,335,96,336,123,335,149,332,169,323,203,318,215,238,336,222,352,     fill=gradient(rgb(133,179,208), 'white', rgb(133,179,208),start='left'),border='black',opacity=polyOpacity)
# Polygon(200,336,15,336,8,233,7,213,10,196,14,176,32,188,49,198,67,207,84,214,98,218,110,221,123,224,137,226,150,228,161,229,175,230,183,230,193,230,201,230,200,230,        199,230,207,230,217,230,225,230,239,229,250,228,263,226,277,224,290,221,302,218,316,214,333,207,351,198,368,188,386,176,390,196,393,213,392,233,385,336,fill=gradient('white', rgb(133,179,208)),border='black',opacity=polyOpacity)

Bezier([(264, 217), (262, 240), (228, 245), (212, 214)], 15)

Bezier([(211, 214), (159, 145), (82, 220), (176, 157)], 15)

# jag.toFront()

app.selectedStartPoint = Circle(app.p0[0], app.p0[1], 5, fill='crimson', border='black', borderWidth=1, visible=False)
app.bezierLine.group.toFront()

app.p0Label.toFront()
app.p1Label.toFront()
app.p2Label.toFront()
app.p3Label.toFront()


def changeStartPoint():
    if app.selectedStart == 1:
        app.selectedStartPoint.centerX = app.p0[0]
        app.selectedStartPoint.centerY = app.p0[1]
    else:
        app.selectedStartPoint.centerX = app.p3[0]
        app.selectedStartPoint.centerY = app.p3[1]
    if app.selectingNewStart:
        app.selectedStartPoint.visible = True
    else:
        app.selectedStartPoint.visible = False



def onKeyPress(key):
    if not app.selectingNewStart and key == 'space':
        app.selectingNewStart = True
        if app.p0[0] > app.p3[0]:
            app.selectedStart = 4
        else:
            app.selectedStart = 1
        changeStartPoint()
        return

    if app.selectingNewStart and key == 'left':
        if app.selectedStart == 1:
            app.selectedStart = 4
        else:
            app.selectedStart = 1
        changeStartPoint()
        return

    if app.selectingNewStart and key == 'right':
        if app.selectedStart == 1:
            app.selectedStart = 4
        else:
            app.selectedStart = 1
        changeStartPoint() 
        return

    if app.selectingNewStart and key == 'enter':
        app.selectingNewStart = False
        app.selectedStartPoint.visible = False
        app.bezierLines.append(app.bezierLine)
        app.bezierLine = Bezier([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        app.lockedPoint = app.selectedStart
        app.bezierLine.group.toFront()
        return


    if key == '0':
        app.bzPoint = 0
        app.selectedPoint.value = 'N'
    elif key == '1':
        app.bzPoint = 1
        app.selectedPoint.value = '1'
    elif key == '2':
        app.bzPoint = 2
        app.selectedPoint.value = '2'
    elif key == '3':
        app.bzPoint = 3
        app.selectedPoint.value = '3'
    elif key == '4':
        app.bzPoint = 4
        app.selectedPoint.value = '4'
    elif key == 'up' or key == '=':
        app.bezierPolygonalPoints += 1
        app.bezierLine.update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        app.polypoints.value = str(app.bezierPolygonalPoints)
    elif key == 'down' or key == '-':
        if app.bezierPolygonalPoints > 2:
            app.bezierPolygonalPoints -= 1
            app.bezierLine.update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
            app.polypoints.value = str(app.bezierPolygonalPoints)
    elif key == 'enter':
        print(f"draw_bezier({[tuple(app.p0), tuple(app.p1), tuple(app.p2), tuple(app.p3)]}, {app.bezierPolygonalPoints})")


def onMouseDrag(x, y):
    if app.bzPoint == 1 and app.lockedPoint != 1:
        app.p0 = Point(x, y)
        app.p0Label.centerX = x
        app.p0Label.centerY = y
        app.p0Label.toFront()
    elif app.bzPoint == 2:
        app.p1 = Point(x, y)
        app.p1Label.centerX = x
        app.p1Label.centerY = y
        app.p1Label.toFront()
    elif app.bzPoint == 3:
        app.p2 = Point(x, y)
        app.p2Label.centerX = x
        app.p2Label.centerY = y
        app.p2Label.toFront()
    elif app.bzPoint == 4 and app.lockedPoint != 4:
        app.p3 = Point(x, y)
        app.p3Label.centerX = x
        app.p3Label.centerY = y
        app.p3Label.toFront()
    app.bezierLine.update([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)



def onStep():
    pass