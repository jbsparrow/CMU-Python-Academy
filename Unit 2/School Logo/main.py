jag = Image('https://cdn.script-ware.net/jag.jpg', 200, 200, opacity=100, align='center')
jag.width = 390
jag.height = 366
jag.centerX = 200
jag.centerY = 200


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


Polygon(200,370,178,352,162,336,82,215,77,203,68,169,65,149,64,123,65,96,67,87,70,84,82,76,94,71,110,66,121,65,    306,71,307,72,318,76,330,84,333,87,335,96,336,123,335,149,332,169,323,203,318,215,238,336,222,352,     fill=gradient(rgb(133,179,208), 'white', rgb(133,179,208),start='left'),border='black',opacity=50)
Polygon(200,336,15,336,8,233,7,213,10,196,14,176,32,188,49,198,67,207,84,214,98,218,110,221,123,224,137,226,150,228,161,229,175,230,183,230,193,230,201,230,200,230,        199,230,207,230,217,230,225,230,239,229,250,228,263,226,277,224,290,221,302,218,316,214,333,207,351,198,368,188,386,176,390,196,393,213,392,233,385,336,fill=gradient('white', rgb(133,179,208)),border='black',opacity=50)
# Arc(200,176,386,90,90,180,fill=None,opacity=30,border='black')
# Arc(8,223,18,48,180,250,fill=None,border='black',opacity=15)
# mirror(Polygon(200,370,162,336,84,214,79,203,fill=None,border='black',opacity=50))



def onStep():
    pass