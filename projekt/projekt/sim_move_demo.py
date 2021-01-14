import sys
#from tkinter import font

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow
from multiprocessing import Queue, Process
from random import randint
from key_notifier import KeyNotifier1
from key_notifier2 import KeyNotifier2
from key_notifier3 import KeyNotifier3
from Force import HeartsMovement
from Pomocni import isHit, generatePrepreka
from GameOver import GameOver
from PreprekaMovement import PreprekaMovement
from Force1 import CoinMovement


class SimMoveDemo(QMainWindow):

    def __init__(self, brojIgraca):
        super().__init__()

        oImage = QImage("slike\\mapa.png")
        sImage = oImage.scaled(QSize(1000, 800))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.auto1 = QPixmap('slike\\auto1.png')
        self.auto2 = QPixmap('slike\\auto2.png')
        self.auto3 = QPixmap('slike\\auto3.png')
        self.preprekademo = QPixmap('slike\\bare.png')

        self.srce = QPixmap('slike\\srce.png')
        self.izadji = QPixmap('slike\\quit.jpg')

        self.prepreka = QPixmap('slike\\prepreka.png')
        self.prepreke = QPixmap('slike\\prepreka.png')
        self.novcic = QPixmap('slike\\redflag.png')

        self.hitSide = False

        self.label1 = QLabel(self)
        self.label11 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.labelPrepreka = QLabel(self)


        self.labelLifes1 = QLabel(self)
        self.labelLifes2 = QLabel(self)
        self.labelLifes3 = QLabel(self)
        self.life1ispis = QLabel(self)
        self.life2ispis = QLabel(self)
        self.life3ispis = QLabel(self)


        self.kraj = None

        self.points1 = QLabel(self)
        self.points11 = QLabel(self)
        self.points2 = QLabel(self)
        self.points22 = QLabel(self)
        self.gameoverLab = QLabel(self)
        self.izlazIzIgre = QLabel(self)

        self.preprekaQueue = Queue()
        self.preprekaProcess = Process(target=generatePrepreka, args=[self.preprekaQueue])
        self.prepreka = []
        self.preprekaProcess.start()

        self.hearts = []

        self.heart = QLabel(self)
        self.heart.setPixmap(self.srce)

        self.coin = QLabel(self)
        self.coin.setPixmap(self.novcic)

        self.prvi = False
        self.drugi = False # da li su pobedili

        self.izgubioPrvi = False
        self.izgubioDrugi = False

        self.poeniPL1 = 0
        self.poeniPL2 = 0

        self.points1.setText('P1: ')
        self.points1.setStyleSheet('color: blue')

        self.points2.setText('P2: ')
        self.points2.setStyleSheet('color: green')

        self.life1ispis.setText('P1 Life: ')
        self.life1ispis.setStyleSheet('color: blue')

        self.life2ispis.setText('P2 Life: ')
        self.life2ispis.setStyleSheet('color: green')

        self.points11.setText(str(self.poeniPL1))
        self.points11.setStyleSheet('color: blue')

        self.points22.setText(str(self.poeniPL2))
        self.points22.setStyleSheet('color: green')

        self.left = 400
        self.top = 200
        self.width = 1000
        self.height = 562

        self.key_notifier = KeyNotifier1()
        self.key_notifier2 = KeyNotifier2()

        if brojIgraca == 2:
            self.key_notifier.key_signal1.connect(self.__update_position__)
            self.key_notifier2.key_signal2.connect(self.__update_position2__)
            self.key_notifier.start()
            self.key_notifier2.start()
            self.brojIgracaDva = True
        else:
            self.brojIgracaDva = False
            self.key_notifier3 = KeyNotifier3()
            self.key_notifier.key_signal1.connect(self.__update_position__)
            self.key_notifier2.key_signal2.connect(self.__update_position2__)
            self.key_notifier3.key_signal3.connect(self.__update_position3__)
            self.key_notifier.start()
            self.key_notifier2.start()
            self.key_notifier3.start()

        self.__init_ui__(brojIgraca)

    def __init_ui__(self, brojIgraca):
        self.setWindowTitle('Crazy cars')

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label1.setPixmap(self.auto1)
        self.label1.setGeometry(250, 400, 50, 100)

        self.label2.setPixmap(self.auto2)
        self.label2.setGeometry(700, 200, 50, 100)

        self.labelPrepreka.setPixmap(self.preprekademo)
        self.labelPrepreka.setGeometry(455, 85, 70, 75)

        self.izlazIzIgre.setPixmap(self.izadji)
        self.izlazIzIgre.setGeometry(940, 0, 60, 60 )
        self.izlazIzIgre.mousePressEvent = self.shutdown

       # self.points1 = 0
       # self.points2 = 0

        self.lives1 = 3
        self.lives2 = 3
        self.lives3 = 3

        self.labelLifes1.setText(str(self.lives1))
        self.labelLifes1.setGeometry(110, 15, 100, 100)
     #   self.labelLifes1.setFont(font)
        self.labelLifes1.setStyleSheet('color: blue')
        self.life1ispis.setGeometry(2, 40, 150, 50)
        # self.life1ispis.setFont(font)

       # self.points1.setGeometry(2, 40, 120, 100)
       # self.points11.setGeometry(110, 40, 100, 100)
        # self.points1.setFont(font)
        self.points1.setStyleSheet('color: blue')
        # self.points1.setFont(font)

        # self.labelLifes2.setText(str(self.lives2))
        # self.life2ispis.setGeometry(2, 85, 120, 100)
        # self.life2ispis.setFont(font)
        self.labelLifes2.setStyleSheet('color: green')
        self.labelLifes2.setGeometry(110, 85, 100, 100)
        # self.labelLifes2.setFont(font)

        self.points2.setGeometry(2, 110, 100, 100)
        self.points2.setGeometry(110, 110, 100, 100)
        # self.points2.setFont(font)
        self.points2.setStyleSheet('color: green')
        #  self.points2.setFont(font)
        self.points2.setStyleSheet('color: green')

        if (brojIgraca == 3):
            self.brojIgracaDva = False

            self.label3.setPixmap(self.auto3)
            self.label3.setGeometry(500, 200, 50, 100)

            self.life1ispis.setGeometry(2, 85, 120, 100)
            self.labelLifes1.setGeometry(110, 85, 100, 100)
            #  self.life1ispis.setFont(font)
            self.life1ispis.setStyleSheet('color: blue')
            self.labelLifes1.setText(str(self.lives2))
            self.labelLifes1.setStyleSheet('color: blue')
            #   self.labelLifes1.setFont(font)

            self.life2ispis.setGeometry(2, 85, 120, 100)
            self.labelLifes2.setGeometry(110, 155, 100, 100)
            # self.life2ispis.setFont(font)
            self.life2ispis.setStyleSheet('color: green')
            self.labelLifes2.setText(str(self.lives2))
            self.labelLifes2.setStyleSheet('color: green')
            # self.labelLifes2.setFont(font)

            self.life3ispis.setGeometry(2, 85, 120, 100)
            self.labelLifes3.setGeometry(110, 225, 100, 100)
            #  self.life3ispis.setFont(font)
            self.life3ispis.setStyleSheet('color: yellow')
            self.labelLifes3.setText(str(self.lives3))
            self.labelLifes3.setStyleSheet('color: yellow')
            # self.labelLifes3.setFont(font)

        self.preprekaMovement = PreprekaMovement()
        self.preprekaMovement.preprekaMovementSignal.connect(self.movePrepreke())
        self.preprekaMovement.start()

        self.coinsMovement = CoinMovement()
        self.coinsMovement.coinsMovementSignal.connect(self.generateForce)
        self.coinsMovement.start()

        self.heartsMovement = HeartsMovement()
        self.heartsMovement.heartsMovementSignal.connect(self.generateForce)
        self.heartsMovement.start()

        self.show()

    def keyPressEvent(self, event):
        a = event.key()
        b = event.key()
        self.key_notifier.add_key(a)
        self.key_notifier2.add_key(b)
        if self.brojIgracaDva == False:
            c = event.key()
            self.key_notifier3.add_key(c)

    def keyReleaseEvent(self, event):
        a = event.key()
        b = event.key()
        self.key_notifier.rem_key(a)
        self.key_notifier2.rem_key(b)
        if self.brojIgracaDva == False:
            c = event.key()
            self.key_notifier3.rem_key(c)

    def __update_position__(self, key):
        rec1 = self.label1.geometry()

        if key == Qt.Key_Right:
            self.label1.setPixmap(self.auto1)
        elif key == Qt.Key_Left:
            self.label1.setPixmap(self.auto1)


        if key == Qt.Key_Right and rec1.x() < 750:
            self.label1.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
        if key == Qt.Key_Down and rec1.y() < 430 :
            self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
        if key == Qt.Key_Up and rec1.y() > 40 :
            self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
        if key == Qt.Key_Left and rec1.x() > 220:
            self.label1.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())



    def __update_position2__(self, key):
        rec2 = self.label2.geometry()

        if key == Qt.Key_D:
            self.label2.setPixmap(self.auto2)
        elif key == Qt.Key_A:
            self.label2.setPixmap(self.auto2)

        if key == Qt.Key_D and rec2.x() < 750:
            self.label2.setGeometry(rec2.x() + 10, rec2.y(), rec2.width(), rec2.height())
        if key == Qt.Key_S and rec2.y() < 430:
            self.label2.setGeometry(rec2.x(), rec2.y() + 10, rec2.width(), rec2.height())
        if key == Qt.Key_W and rec2.y() > 40:
            self.label2.setGeometry(rec2.x(), rec2.y() - 10, rec2.width(), rec2.height())
        if key == Qt.Key_A and rec2.x() > 220:
            self.label2.setGeometry(rec2.x() - 10, rec2.y(), rec2.width(), rec2.height())




    def __update_position3__(self, key):
        rec3 = self.label3.geometry()

        if key == Qt.Key_6:
            self.label3.setPixmap(self.auto3)
        elif key == Qt.Key_4:
            self.label3.setPixmap(self.auto3)

        if key == Qt.Key_6 and rec3.x() < 750:
            self.label3.setGeometry(rec3.x() + 10, rec3.y(), rec3.width(), rec3.height())
        if key == Qt.Key_5 and rec3.y() < 430:
            self.label3.setGeometry(rec3.x(), rec3.y() + 10, rec3.width(), rec3.height())
        if key == Qt.Key_8 and rec3.y() > 40:
            self.label3.setGeometry(rec3.x(), rec3.y() - 10, rec3.width(), rec3.height())
        if key == Qt.Key_4 and rec3.x() > 220:
            self.label3.setGeometry(rec3.x() - 10, rec3.y(), rec3.width(), rec3.height())




     def movePrepreke(self):
        rec = self.label4.geometry()

        a = randint(0, 100)
        if a % 12 == 0:

            prepreka = QLabel(self)
            self.prepreke.append(prepreka)
            self.prepreke[len(self.prepreke) - 1].setPixmap(self.pix4)
            self.prepreke[len(self.prepreke) - 1].setGeometry(rec.x(), rec.y(), 40, 40)
            self.prepreke[len(self.prepreke) - 1].show()

        for prepreka in self.prepreke:
            recp = prepreka.geometry()
            prepreka.setGeometry(recp.x(), recp.y() + 10, recp.width(), recp.height())

            if recp.y() > 600:
                prepreka.hide()
                self.prepreke.remove(prepreka)

            if isHit(prepreka, self.label1):
                if self.lives1 > 0:
                    self.lives1 -= 1
                    self.labelLifes1.setText(str(self.lives1))
                    prepreka.hide()
                    self.prepreke.remove(prepreka)

                    if self.lives1 == 0:
                        if self.brojIgracaDva:
                            self.kraj = GameOver(1, self.poeniPL1)
                            self.close()
                        else:
                            self.label1.setGeometry(200, 475, 75, 75)
                            self.label1.hide()

                            if self.izgubioDrugi:
                                self.kraj = GameOver(1, self.poeniPL1)
                                self.close()
                            else:
                                self.izgubioPrvi = True

            if isHit(prepreka, self.label30):
                if self.lives2 > 0:
                    self.lives2 -= 1
                    self.labelLifes2.setText(str(self.lives2))
                    prepreka.hide()
                    self.prepreke.remove(prepreka)

                    if self.lives2 == 0:
                        self.label30.setGeometry(200, 475, 75, 75)
                        self.label30.hide()

                        if self.izgubioPrvi:
                            self.kraj = GameOver(2, self.poeniPL2)
                            self.close()
                        else:
                            self.izgubioDrugi = True



    def generateForce(self):

        self.heart.setGeometry(randint(240, 760), randint(100, 500), 40, 40)
        self.heart.show()

        self.timerP3 = QTimer(self)
        self.timerP3.start(7000)
        self.timerP3.timeout.connect(self.hideForce)

        #for heart in self.hearts:
        if isHit(self.heart, self.label1):
            self.lives1 += 1
            self.labelLifes1.setText(str(self.lives1))
            self.heart.hide()
            #self.hearts.remove(heart)

            if self.lives1 == 0:
                if self.brojIgracaDva:
                    self.kraj = GameOver(1, self.poeniPL1)
                    self.close()
                else:
                    self.label1.setGeometry(200, 40, 75, 75)
                    self.label1.hide()
                    self.lives1 = 0
                    self.labelLifes1.setText(str(self.lives1))

                    if self.izgubioDrugi:
                        self.kraj = GameOver(1, self.poeniPL1)
                        self.close()
                    else:
                        self.izgubioPrvi = True

        if isHit(self.heart, self.label2):
            self.lives2 += 1
            self.labelLifes2.setText(str(self.lives2))
            self.heart.hide()
            #self.hearts.remove(heart)

            if self.lives2 == 0:
                self.lives2 = 0
                self.labelLifes2.setText(str(self.lives2))
                self.label30.setGeometry(200, 40, 75, 75)
                self.label30.hide()

                if self.izgubioPrvi:
                    self.kraj = GameOver(2, self.poeniPL2)
                    self.close()
                else:
                    self.izgubioDrugi = True

    def generateForce1(self):

        self.coin.setGeometry(randint(240, 760), randint(100, 500), 40, 40)
        self.coin.show()

        self.timerP4 = QTimer(self)
        self.timerP4.start(7000)
        self.timerP4.timeout.connect(self.hideForce1)

        #for heart in self.hearts:
        if isHit(self.coin, self.label1):
            self.points += 1
            self.labelPoints1.setText(str(self.points1))
            self.coin.hide()

        if isHit(self.coin, self.label30):
            self.points2 += 1
            self.labelPoints2.setText(str(self.lives2))
            self.points.hide()

    def hideForce(self):
        self.heart.hide()

    def hideForce1(self):
            self.coin.hide()

    def closeEvent(self, event):
        self.coinsMovement.die()
        self.heartsMovement.die()
        self.preprekaProcess.terminate()
        self.preprekaMovement.die()
        self.key_notifier.die()
        self.key_notifier2.die()
        self.key_notifier3.die()

    def shutdown(self, event):
        self.preprekaProcess.terminate()
        self.close()

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = SimMoveDemo(1,1)
     sys.exit(app.exec_())