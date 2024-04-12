import math

jag = Image('https://cdn.script-ware.net/jag.jpg', 200, 200, opacity=50, align='center')
jag.width = 390
jag.height = 366
jag.centerX = 200
jag.centerY = 200

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

def cubic_bezier(t: int, P0: tuple, P1: tuple, P2: tuple, P3: tuple) -> tuple:
    """Calculate the point on the cubic Bezier curve for current time(t)."""
    x = (1 - t)**3 * P0[0] + 3 * (1 - t)**2 * t * P1[0] + 3 * (1 - t) * t**2 * P2[0] + t**3 * P3[0]
    y = (1 - t)**3 * P0[1] + 3 * (1 - t)**2 * t * P1[1] + 3 * (1 - t) * t**2 * P2[1] + t**3 * P3[1]
    return (x, y)

def draw_bezier(control_points: list[tuple], num_segments: int) -> Polygon:
    """Draws a bezier curve with the specified control points and segments."""
    P0, P1, P2, P3 = control_points
    points = [cubic_bezier(t / num_segments, P0, P1, P2, P3) for t in range(num_segments + 1)]
    shape = Polygon(0,0,1,1,fill=rgb(67,67,67),border='black',opacity=60)
    pointList = [[x, y] for x, y in points]
    setattr(shape, 'pointList', pointList)
    return shape

app.bezier = draw_bezier([app.p0,app.p1,app.p2,app.p3],15)

def draw_bezier_sketch(control_points: list[tuple], num_segments:int) -> None:
    """Draws a bezier curve with the specified control points and segments that is to be used for designing the drawing. Points can be exported by pressing return."""
    P0, P1, P2, P3 = control_points
    points = [cubic_bezier(t / num_segments, P0, P1, P2, P3) for t in range(num_segments + 1)]
    pointList = [[x, y] for x, y in points]
    setattr(app.bezier, 'pointList', pointList)
    return None

def create_bezier_group(control_points, num_segments):
    """Create a group of line segments to represent the Bezier curve."""
    P0, P1, P2, P3 = control_points
    points = [cubic_bezier(t / num_segments, P0, P1, P2, P3) for t in range(num_segments + 1)]
    bezier_group = Group()
    for i in range(len(points) - 1):
        line = Line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
        bezier_group.add(line)
    return bezier_group

def update_bezier_group(bezier_group, control_points, num_segments):
    """Efficiently update the group of line segments for the Bezier curve."""
    P0, P1, P2, P3 = control_points
    points = [cubic_bezier(t / num_segments, P0, P1, P2, P3) for t in range(num_segments + 1)]
    current_lines = len(bezier_group.children)
    
    # Update existing lines or add new ones if necessary
    for i,line in enumerate(bezier_group.children):
        if i < current_lines:
            line.x1 = points[i][0]
            line.y1 = points[i][1]
            line.x2 = points[i + 1][0]
            line.y2 = points[i + 1][1]
        else:
            new_line = Line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
            bezier_group.add(new_line)
    
    # Remove excess lines if the number of segments decreased
    while current_lines > num_segments:
        bezier_group.remove(bezier_group.getChild(current_lines - 1))
        current_lines -= 1


app.bezierLine = create_bezier_group([app.p0,app.p1,app.p2,app.p3],15)

class mirror():
    def __init__(self, shape):
        self.shape = shape
        self.mirroredShape = self.mirrorShape()
        return self.mirroredShape

    def insertAttributes(self, shape, dict: dict):
        for key, value in dict.items():
            try:
                setattr(shape, key, value)
            except:
                pass
        return shape


    def mirrorRect(self, rect):
        shapeAttributes = {'fill': rect.fill, 'border': rect.border, 'borderWidth': rect.borderWidth, 'opacity': rect.opacity, 'dashes': rect.dashes, 'centerX': 400 - rect.centerX, 'centerY': rect.centerY}
        newShape = Line(0, 0, rect.width, rect.height)
        return self.insertAttributes(newShape, shapeAttributes)

    def mirrorOval(self, oval):
        shapeAttributes = {'fill': oval.fill, 'border': oval.border, 'borderWidth': oval.borderWidth, 'opacity': oval.opacity, 'dashes': oval.dashes, 'centerX': 400 - oval.centerX, 'centerY': oval.centerY}
        newShape = Oval(0, 0, oval.width, oval.height)
        return self.insertAttributes(newShape, shapeAttributes)

    def mirrorCircle(self, circle):
        shapeAttributes = {'fill': circle.fill, 'border': circle.border, 'borderWidth': circle.borderWidth, 'opacity': circle.opacity, 'dashes': circle.dashes, 'centerX': 400 - circle.centerX, 'centerY': circle.centerY}
        newShape = Circle(0, 0, circle.radius)
        return self.insertAttributes(newShape, shapeAttributes)

    def mirrorLine(self, line):
        shapeAttributes = {'arrowStart': line.arrowEnd, 'arrowEnd': line.arrowStart, 'fill': line.fill, 'border': line.border, 'borderWidth': line.borderWidth, 'opacity': line.opacity, 'dashes': line.dashes}
        newShape = Line(400 - line.x1, line.y1, 400 - line.x2, line.y2)
        return self.insertAttributes(newShape, shapeAttributes)

    def mirrorLabel(self, label):
        shapeAttributes = {'size': label.size, 'font': label.font, 'bold': label.bold, 'italic': label.italic, 'fill': label.fill, 'border': label.border, 'borderWidth': label.borderWidth, 'opacity': label.opacity, 'dashes': label.dashes, 'centerX': 400 - label.centerX, 'centerY': label.centerY}
        newShape = Label(label.value, 0, 0)
        return self.insertAttributes(newShape, shapeAttributes)

    def mirrorRegularPolygon(self, regularPolygon):
        shapeAttributes = {'fill': regularPolygon.fill, 'border': regularPolygon.border, 'borderWidth': regularPolygon.borderWidth, 'opacity': regularPolygon.opacity, 'dashes': regularPolygon.dashes, 'centerX': 400 - regularPolygon.centerX, 'centerY': regularPolygon.centerY}
        newShape = RegularPolygon(0, 0, regularPolygon.radius, regularPolygon.points)
        return self.insertAttributes(newShape, shapeAttributes)

    def mirrorStar(self, star):
        shapeAttributes = {'fill': star.fill, 'border': star.border, 'borderWidth': star.borderWidth, 'roundness': star.roundness, 'opacity': star.opacity, 'dashes': star.dashes, 'centerX': 400 - star.centerX, 'centerY': star.centerY}
        newShape = Star(0, 0, star.radius, star.points)
        return self.insertAttributes(newShape, shapeAttributes)

    def mirrorPolygon(self, polygon):
        shapeAttributes = {'fill': polygon.fill, 'border': polygon.border, 'borderWidth': polygon.borderWidth, 'opacity': polygon.opacity, 'dashes': polygon.dashes}
        points = polygon.pointList # structure: [[x1, y1], [x2, y2], ...]
        newPoints = []
        for point in points:
            newPoints.append(400 - point[0])
            newPoints.append(point[1])
            # newPoints.append(400 - point[0])
        newShape = Polygon(*newPoints)
        # print(newPoints[::-1])
        return self.insertAttributes(newShape, shapeAttributes)

    def mirrorArc(self, arc):
        shapeAttributes = {'fill': arc.fill, 'border': arc.border, 'borderWidth': arc.borderWidth, 'opacity': arc.opacity, 'dashes': arc.dashes, 'centerX': 400 - arc.centerX, 'centerY': arc.centerY, 'width': arc.width, 'height': arc.height}
        newShape = Arc(0, 0, arc.width*2, arc.height*2, arc.startAngle+180, arc.sweepAngle)
        return self.insertAttributes(newShape, shapeAttributes)


    def mirrorShape(self, shape=None):
        if shape != None:
            self.shape = shape
        if isinstance(self.shape, Group):
            mirroredShapes = Group()
            for child in self.shape.children:
                mirroredShapes.add(self.mirrorShape(child))
            return mirroredShapes
        elif isinstance(self.shape, Rect):
            return self.mirrorRect(self.shape)
        elif isinstance(self.shape, Oval):
            return self.mirrorOval(self.shape)
        elif isinstance(self.shape, Circle):
            return self.mirrorCircle(self.shape)
        elif isinstance(self.shape, Line):
            return self.mirrorLine(self.shape)
        elif isinstance(self.shape, Label):
            return self.mirrorLabel(self.shape)
        elif isinstance(self.shape, RegularPolygon):
            return self.mirrorRegularPolygon(self.shape)
        elif isinstance(self.shape, Star):
            return self.mirrorStar(self.shape)
        elif isinstance(self.shape, Polygon):
            return self.mirrorPolygon(self.shape)
        elif isinstance(self.shape, Arc):
            return self.mirrorArc(self.shape)

polyOpacity = 100
# Polygon(200,370,178,352,162,336,82,215,77,203,68,169,65,149,64,123,65,96,67,87,70,84,82,76,94,71,110,66,121,65,    306,71,307,72,318,76,330,84,333,87,335,96,336,123,335,149,332,169,323,203,318,215,238,336,222,352,     fill=gradient(rgb(133,179,208), 'white', rgb(133,179,208),start='left'),border='black',opacity=polyOpacity)
# Polygon(200,336,15,336,8,233,7,213,10,196,14,176,32,188,49,198,67,207,84,214,98,218,110,221,123,224,137,226,150,228,161,229,175,230,183,230,193,230,201,230,200,230,        199,230,207,230,217,230,225,230,239,229,250,228,263,226,277,224,290,221,302,218,316,214,333,207,351,198,368,188,386,176,390,196,393,213,392,233,385,336,fill=gradient('white', rgb(133,179,208)),border='black',opacity=polyOpacity)

draw_bezier([(264, 217), (262, 240), (228, 245), (212, 214)], 15)

draw_bezier([(211, 214), (159, 145), (82, 220), (176, 157)], 15)

jag.toFront()

def onKeyPress(key):
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
        # draw_bezier_sketch([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        update_bezier_group(app.bezierLine, [app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
        app.polypoints.value = str(app.bezierPolygonalPoints)
    elif key == 'down' or key == '-':
        if app.bezierPolygonalPoints > 2:
            app.bezierPolygonalPoints -= 1
            # draw_bezier_sketch([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
            update_bezier_group(app.bezierLine, [app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
            app.polypoints.value = str(app.bezierPolygonalPoints)
    elif key == 'enter':
        print(f"draw_bezier({[tuple(app.p0), tuple(app.p1), tuple(app.p2), tuple(app.p3)]}, {app.bezierPolygonalPoints})")


def onMouseDrag(x, y):
    if app.bzPoint == 1:
        app.p0 = Point(x, y)
        app.p0Label.centerX = x
        app.p0Label.centerY = y
    elif app.bzPoint == 2:
        app.p1 = Point(x, y)
        app.p1Label.centerX = x
        app.p1Label.centerY = y
    elif app.bzPoint == 3:
        app.p2 = Point(x, y)
        app.p2Label.centerX = x
        app.p2Label.centerY = y
    elif app.bzPoint == 4:
        app.p3 = Point(x, y)
        app.p3Label.centerX = x
        app.p3Label.centerY = y
    # draw_bezier_sketch([app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)
    update_bezier_group(app.bezierLine, [app.p0, app.p1, app.p2, app.p3], app.bezierPolygonalPoints)



def onStep():
    pass