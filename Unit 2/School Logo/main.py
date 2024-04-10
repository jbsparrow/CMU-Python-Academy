jag = Image('https://cdn.script-ware.net/jag.jpg', 200, 200, opacity=5, align='center')
jag.width = 390
jag.height = 366
jag.centerX = 200
jag.centerY = 200


class mirror():
    def __init__(self, shape):
        self.shape = shape
        self.mirrorShape()

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
            newPoints.append([400 - point[0], point[1]])
        newShape = Polygon(*newPoints)
        return self.insertAttributes(newShape, shapeAttributes)

    def mirrorArc(self, arc):
        shapeAttributes = {'fill': arc.fill, 'border': arc.border, 'borderWidth': arc.borderWidth, 'opacity': arc.opacity, 'dashes': arc.dashes, 'centerX': 400 - arc.centerX, 'centerY': arc.centerY}
        newShape = Arc(0, 0, arc.width*2, arc.height*2, arc.startAngle-90, arc.sweepAngle)
        return self.insertAttributes(newShape, shapeAttributes)


    def mirrorShape(self):
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


Line(15,336,385,336)
w=Line(15,336,8,233)
w2 = mirror(w)
o = Arc(200, 200, 200, 100, 0, 180, opacity=20)
m = mirror(o)



# shapeList = [Rect(200, 200, 20, 40), Oval(200, 200, 60, 30), Circle(200, 200, 20), Line(0, 200, 400, 200, arrowStart=True, arrowEnd=True), Label('Hello World', 200, 50, size=18), RegularPolygon(200, 200, 20, 3), Star(200, 200, 30, 5), Polygon(25, 25, 150, 25, 200, 200, 100, 250, 25, 200), Arc(200, 200, 200, 100, 0, 90)]

def onStep():
    pass