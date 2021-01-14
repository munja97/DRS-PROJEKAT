import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton


class GameOver(QMainWindow):

    def __init__(self, br, sc):
        super().__init__()

        oImage = QImage("slike\\game_over.jpg")
        self.label = QLabel(self)
        self.who_is_winner = QLabel(self)
        self.who_is_winner1 = QPixmap('slike\\player1_pobednik.png.png')
        self.who_is_winner2 = QPixmap('slike\\player2_pobednik .png.png')
        self.left = 400
        self.top = 200
        self.width = 450
        self.height = 470
        palette = QPalette()
        sImage = oImage.scaled(QSize(450, 470))
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.__init_ui__(br)

    def __init_ui__(self, br):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon('slike\\ikonica.jpg'))
        #self.setWindowState(Qt.WindowFullScreen)

        self.setWindowTitle("Game Over")

        if(br==1):
            self.who_is_winner.setPixmap(self.who_is_winner1)
            self.who_is_winner.setGeometry(35, 250, 395, 43)
        else:
            self.who_is_winner.setPixmap(self.who_is_winner2)
            self.who_is_winner.setGeometry(35, 250, 395, 43)

        button4 = QPushButton('QUIT', self)
        button4.resize(200, 30)
        button4.move(135, 316)

        button4.clicked.connect(self.quit_on_click)
        self.show()

    def quit_on_click(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameOver(1, 1)
    sys.exit(app.exec_())