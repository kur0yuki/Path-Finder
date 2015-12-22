__author__ = 'catherine'

import sys, random
from heapq import heappush, heappop
from PyQt5 import QtWidgets, QtCore, QtGui


class vertex:
    table = []

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.d = 999999999
        self.parent = 0
        self.successors = []

    def dist(self, other):
        return self.table[other.x][other.y]

    def relax(self, other):
        if (self.d > other.d + self.dist(other)):
            path.vert[self.x][self.y].d = other.d + self.dist(other)
            path.vert[self.x][self.y].parent = other

    def __add__(self, other):
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def next(self, path):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    tmp = vertex(self.x + i, self.y + j)
                    if (tmp.x >= 0 and tmp.y >= 0 and
                                tmp.x < 40 and tmp.y < 30):
                        tmp = path.vert[self.x + i][j + self.y]
                        self.successors.append(tmp)
        return self.successors

    def __lt__(self, other):
        return self.d.__lt__(other.d)


class path:
    vert = vq = []
    table = []
    begin = 0
    stop = 0

    def __init__(self, table=[], begin=0, stop=0):
        path.table = table
        path.begin = begin
        path.stop = stop

    def find(self, vert):
        s = set()
        self.queue(vert)
        while (self.vq != []):
            u = heappop(self.vq)
            if (u.x, u.y)==(self.begin.x, self.begin.y): break
            s.add(u)
            for v in u.next(self):
                if (v.x, v.y) != (self.stop.x, self.stop.y):
                    v.relax(u)
                    self.vq.sort()
        return self.vert

    def init(self, table):
        vertex.table[self.stop.x][self.stop.y] = 0
        for i in range(len(table)):
            path.vert.append([])
            for j in range(len(table[i])):
                tmp = vertex(i, j)
                if (i, j) == (self.stop.x, self.stop.y):
                    tmp.d = 0
                    tmp.parent = 0
                path.vert[-1].append(tmp)

    def queue(self, vert):
        self.vq = []
        for tmp in vert:
            for tmp1 in tmp:
                heappush(self.vq, tmp1)


def haupt(table, begin, stop):
    stop.d = 0
    p = path(table, begin, stop)
    p.init(table)
    p.find(p.vert)
    fin = p.vert[begin.x][begin.y]
    vrt = []
    while ((fin.x, fin.y) != (stop.x, stop.y)):
        fin = fin.parent
        if fin == 0: break
        vrt.append(fin)
    return vrt


class onceMore(QtWidgets.QWidget):
    click = 0
    rects = []
    weights = []
    pathF = []

    def __init__(self):
        super().__init__()
        self.rect()
        self.initUI()

    def rect(self):
        for i in range(40):
            weightRow = []
            for j in range(30):
                rect = QtCore.QRectF(i * 15, j * 15, 15, 15)
                colour = random.randint(0, 255)
                self.rects.append([rect, colour])
                weightRow.append(255 - colour)
            self.weights.append(weightRow)

    def initUI(self):
        self.setGeometry(100, 100, 600, 450)
        self.setWindowTitle("Prak 2")
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        for coloredrect in self.rects:
            rect = coloredrect[0]
            colour = coloredrect[1]
            painter.fillRect(rect, QtGui.QColor(colour, colour, colour))
            painter.drawRect(rect)
        if (self.click > 0):
            x1 = self.beginP.x()
            y1 = self.beginP.y()
            painter.fillRect(
                    QtCore.QRectF(x1 - x1 % 15, y1 - y1 % 15, 15, 15),
                    QtGui.QColor(0, 255, 0))
        if (self.click > 1):
            x1 = self.endP.x()
            y1 = self.endP.y()
            painter.fillRect(
                    QtCore.QRectF(x1 - x1 % 15, y1 - y1 % 15, 15, 15),
                    QtGui.QColor(255, 0, 0))
        if (self.pathF != []):
            for square in self.pathF:
                x1 = square.x * 15
                y1 = square.y * 15
                painter.fillRect(
                        QtCore.QRectF(x1 - x1 % 15, y1 - y1 % 15, 15, 15),
                        QtGui.QColor(0, 0, 255))
        painter.end()

    def mousePressEvent(self, event):
        self.x = x = event.x()
        self.y = y = event.y()
        self.click += 1
        if (self.click == 1):
            self.beginP = event.pos()
        elif (self.click == 2):
            self.endP = event.pos()
            self.path = self.findPath(self.beginP, self.endP)
        self.update()

    def findPath(self, be, en):
        print(be, en)
        vertex.table = self.weights
        be = vertex(int(be.x() / 15), int(be.y() / 15))
        en = vertex(int(en.x() / 15), int(en.y() / 15))
        self.pathF = haupt(self.weights, be, en)
        self.update()


app = QtWidgets.QApplication(sys.argv)

ex = onceMore()

sys.exit(app.exec_())
