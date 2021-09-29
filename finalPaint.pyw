
"""
@author: Tsega Tsewameskel
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Painter"

        self.randomName = open("random.txt", "w")
        self.setWindowTitle(title)
        self.setFixedSize(950, 650)
        self.setWindowIcon(QIcon("icon.png"))
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.brushSize = 4
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        clearMenu = mainMenu.addMenu("Clear")
        brushS = mainMenu.addMenu("Brush Size")
        brushC = mainMenu.addMenu("Brush Color")

        saveA = QAction("Save", self)
        fileMenu.addAction(saveA)
        saveA.triggered.connect(self.save)

        closeA = QAction("Close", self)
        fileMenu.addAction(closeA)
        closeA.triggered.connect(self.close)

        clearA = QAction("Clear Drawing", self)
        clearA.setShortcut("Ctrl + X")
        clearMenu.addAction(clearA)
        clearA.triggered.connect(self.clear)

        pix3 = QAction("3px", self)
        brushS.addAction(pix3)
        pix3.triggered.connect(self.pixel3)

        pix6 = QAction("6px", self)
        brushS.addAction(pix6)
        pix6.triggered.connect(self.pixel6)

        pix9 = QAction("9px", self)
        brushS.addAction(pix9)
        pix9.triggered.connect(self.pixel9)

        pix12 = QAction("12px", self)
        brushS.addAction(pix12)
        pix12.triggered.connect(self.pixel12)

        pix30 = QAction("30px", self)
        brushS.addAction(pix30)
        pix30.triggered.connect(self.pixel30)

        white = QAction("White", self)
        brushC.addAction(white)
        white.triggered.connect(self.whiteC)

        black = QAction("Black", self)
        brushC.addAction(black)
        black.triggered.connect(self.blackC)

        red = QAction("Red", self)
        brushC.addAction(red)
        red.triggered.connect(self.redC)

        green = QAction("Green", self)
        brushC.addAction(green)
        green.triggered.connect(self.greenC)

        blue = QAction("Blue", self)
        brushC.addAction(blue)
        blue.triggered.connect(self.blueC)

    def closeEvent(self, event):
        msgB = QMessageBox()
        msgB.setText(
            "Confirmation message: Are you sure you want to close the program? All work will be lost upon exit.")
        msgB.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
        msgB.setDefaultButton(QMessageBox.Yes)
        if msgB.exec_() == QMessageBox.Yes:
            event.accept()
            self.randomName.close()
        else:
            event.ignore()

    def save(self):
        saveDirectory, _ = QFileDialog.getSaveFileName(self, "Save Paint",
                                                  "", "PNG(*.png);;JPEG(*.jpg *.jpeg);; All Files(*.*) ")
        if saveDirectory == "":
            return
        self.image.save(saveDirectory)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def pixel3(self):
        self.brushSize = 4

    def pixel6(self):
        self.brushSize = 6

    def pixel9(self):
        self.brushSize = 9

    def pixel12(self):
        self.brushSize = 12

    def pixel30(self):
        self.brushSize = 30

    def whiteC(self):
        self.brushColor = Qt.white

    def blackC(self):
        self.brushColor = Qt.black

    def redC(self):
        self.brushColor = Qt.red

    def greenC(self):
        self.brushColor = Qt.green

    def blueC(self):
        self.brushColor = Qt.blue

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            self.randomName.write("(%d,%d)\n" % (event.pos().x(), event.pos().y()))

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize))  # Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.randomName.write("(%d,%d)\n" % (event.pos().x(), event.pos().y()))
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter()
        canvasPainter.begin(self)
        canvasPainter.drawImage(self.rect(), self.image)
        canvasPainter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
