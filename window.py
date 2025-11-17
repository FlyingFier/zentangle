import sys
import zentangle
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QLineEdit, QPushButton, QFrame
)
from PySide6.QtGui import QMouseEvent, QColor, QPalette, QPainter, QCursor, Qt
from PySide6.QtSvgWidgets import QSvgWidget

class ClickArea(QFrame):

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.points = []
        self.is_closed = False
        self.active = None
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#f8f8f8"))  # lighter
        self.setAutoFillBackground(True)
        self.setPalette(pal)

    def mousePressEvent(self, e):
        pos = e.position().toPoint()
        for i, pt in enumerate(self.points):
            if (pt - pos).manhattanLength() < 8:
                if i == 0 and not self.is_closed and len(self.points) > 2:
                    self.is_closed = True
                    self.update()
                self.active = i
                return
        self.points.append(pos)
        self.update()

    def mouseMoveEvent(self, e):
        if self.active is not None and e.buttons() & Qt.LeftButton:
            self.points[self.active] = e.position().toPoint()
            self.update()
            return

        pos = e.position().toPoint()
        hover = None

        for pt in self.points:
            if (pt - pos).manhattanLength() < 8:
                hover = pt
                break

        if hover:
            self.setCursor(QCursor(Qt.PointingHandCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))


    def mouseReleaseEvent(self, _):
        self.active = None

    def paintEvent(self, _):
        p = QPainter(self)
        p.setBrush(QColor("black"))
        for pt in self.points:
            p.drawEllipse(pt, 3, 3)
            p.setPen(QColor("black"))
        for i in range(len(self.points) - 1):
            p.drawLine(self.points[i], self.points[i + 1])
        if self.is_closed:
            p.drawLine(self.points[-1], self.points[0])

    def clear_points(self):
        self.is_closed = False
        self.points = []


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.init()
        self.svg_windows = []

    def clear_points(self, area):
        area.clear_points()
        area.update()

    def show_svg(self, drawing):
        data = drawing.tostring().encode("utf-8")

        w = QWidget()
        layout = QVBoxLayout(w)

        svg = QSvgWidget()
        svg.load(data)
        layout.addWidget(svg)

        w.resize(480, 480)
        w.show()
        return w

    def zen(self, points, steps):
        xy_points = [(pt.x(), pt.y()) for pt in points]
        self.svg_windows.append(self.show_svg(zentangle.zentanlge_from_points(xy_points, int(steps))))

    def init(self):
        self.setWindowTitle("UI")
        self.setFixedSize(640, 480)

        root = QHBoxLayout(self)

        sidebar = QWidget()
        sidebar.setFixedWidth(160)
        side_layout = QVBoxLayout(sidebar)

        steps = QLineEdit()
        steps.setPlaceholderText("steps")
        zen = QPushButton("Zen")
        zen.clicked.connect(lambda: self.zen(area.points, steps.text()))
        clear = QPushButton("Clear")
        clear.clicked.connect(lambda: self.clear_points(area))

        side_layout.addWidget(steps)
        side_layout.addWidget(zen)
        side_layout.addWidget(clear)
        side_layout.addStretch()

        area = ClickArea()

        root.addWidget(sidebar)
        root.addWidget(area)


def main():
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()