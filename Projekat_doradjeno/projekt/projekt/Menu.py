import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton
from sim_move_demo import SimMoveDemo
from PyQt5.QtCore import Qt

class Menu(QMainWindow):

    def __init__(self):
        super().__init__()

        oImage = QImage("slike\\naslov.jpg")

        self.label = QLabel(self)
        self.label2Player = QLabel(self)
        self.twoplayers = QPixmap('slike\\dvaigraca.png')

        self.label3Player = QLabel(self)
        self.moreplayers = QPixmap('slike\\viseigraca.png')

        self.left = 400
        self.top = 200
        self.width = 1000
        self.height = 562

        palette = QPalette()
        sImage = oImage.scaled(QSize(1000, 562))
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.__init_ui__()

    def __init_ui__(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon('slike\\ikonica.jpg'))

        self.setWindowTitle("Menu")

        self.label2Player.setPixmap(self.twoplayers)
        self.label2Player.setGeometry(320, 320, 395, 43)
        self.label2Player.mousePressEvent = self.two_players_on_click

        self.label3Player.setPixmap(self.moreplayers)
        self.label3Player.setGeometry(320, 370, 395, 43)
        self.label3Player.mousePressEvent = self.more_players_on_click

        button4 = QPushButton('QUIT', self)
        button4.resize(395, 43)
        button4.move(320, 420)
        button4.clicked.connect(self.quit_on_click)

        self.show()

    def two_players_on_click(self, event):
        self.twoplayers = SimMoveDemo(2)
       # self.two.show()
        self.hide()

    def more_players_on_click(self, event):
        self.moreplayers = SimMoveDemo(3)
       # self.more.show()
        self.hide()

    def quit_on_click(self):
        self.close()        #izlaz

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())
