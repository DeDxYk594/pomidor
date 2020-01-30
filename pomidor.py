from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QRectF, QPoint, QPointF
from PyQt5.QtGui import QIcon, QPainter, QConicalGradient, QBrush, QColor, QFont, QPen
from PyQt5.QtMultimedia import QSound
from sys import argv


FINAL_SOUND_PATH="smb_gameover.wav"

class TomatoTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("logo.jpg"))
        self.setWindowTitle("Помидор - приложение для тайм-менеджмента")

        try:
            settings = open("settings.ini", "r")
            self.default_time = int(settings.read())
            settings.close()
        except:
            settings = open("settings.ini", "w")
            settings.write("1500")
            settings.close()
            self.default_time = 1500

        self.current_time = self.default_time
        self.is_active = 0
        self.font = None
        self.taps=0

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

        self.alarmSound=QSound(FINAL_SOUND_PATH)

        # До этой отметки виджеты не ставить! На этой отметке должны быть заданы все локальные переменные, которые будут в self.drawWidget!
        super().__init__()
        self.show()

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, painter):
        # Поиск лучшего местоположения для томата

        size = self.size()
        x, y = size.width(), size.height()

        sec = self.current_time % 60
        min = self.current_time // 60

        angle = self.current_time / self.default_time
        if sec and min:
            rend_text = "{}:{}".format(min, sec)
        elif sec:
            rend_text = "{}".format(sec)
        elif min:
            rend_text = "{}:0".format(min)
        else:
            rend_text = "0"
            self.is_active = 0
            self.current_time = self.default_time
            self.alarmSound.play()
        if x < y - 70:

            center = (x / 2, (y - 20) / 2 + 20)
            notcenter = x / 2 - 20
        else:
            center = (x / 2, y / 2 + 20)
            notcenter = y / 2 - 60

        gradient = QConicalGradient(QPointF(*center), 0)
        gradient.setAngle(90)

        gradient.setColorAt(0, QColor("911e42"))
        if angle != 1 or not self.is_active:
            gradient.setColorAt(1, QColor("#4a75c1"))

        if self.is_active:
            gradient.setColorAt(angle, QColor("#9c7130"))

        brush = QBrush(gradient)
        painter.setBrush(brush)

        self.centerx = center[0]
        self.highy = center[1] - notcenter

        self.font = QFont("Helvetica [Cronyx]", int(notcenter / 6))
        painter.setFont(self.font)
        painter.drawEllipse(QPointF(*center), notcenter, notcenter)

        pen = QPen(QColor("#111100"))
        painter.setPen(pen)

        painter.drawText(*center, rend_text)

        gradient = QConicalGradient(QPointF(x / 4, self.highy / 2), 0)
        gradient.setAngle(90)
        gradient.setColorAt(0, QColor("#faff53"))
        gradient.setColorAt(0.125, QColor("#23c900"))
        gradient.setColorAt(0.25, QColor("#faff53"))
        gradient.setColorAt(0.375, QColor("#23c900"))
        gradient.setColorAt(0.5, QColor("#faff53"))
        gradient.setColorAt(0.625, QColor("#23c900"))
        gradient.setColorAt(0.75, QColor("#faff53"))
        gradient.setColorAt(0.875, QColor("#23c900"))
        gradient.setColorAt(1, QColor("#faff53"))
        painter.setBrush(gradient)
        painter.drawRect(QRectF(QPoint(0, 0), QPoint(self.centerx, self.highy - 1)))

        gradient = QConicalGradient(QPointF(x * 3 / 4, self.highy / 2), 0)
        gradient.setColorAt(0, QColor("#fff0f0"))
        gradient.setColorAt(0.1, QColor("#f4432a"))
        gradient.setColorAt(0.4, QColor("#f4432a"))
        gradient.setColorAt(0.5, QColor("#fff0f0"))
        gradient.setColorAt(0.6, QColor("#f4432a"))
        gradient.setColorAt(0.9, QColor("#f4432a"))
        gradient.setColorAt(1, QColor("#fff0f0"))
        painter.setBrush(gradient)
        painter.drawRect(QRectF(QPoint(x, 0), QPoint(self.centerx, self.highy - 1)))

    def tick(self):

        if self.is_active:
            self.current_time -= 1
        self.repaint()

    def closeEvent(self, QCloseEvent):
        QCloseEvent.accept()
        pass

    def mousePressEvent(self, QMouseEvent):

        x,y=QMouseEvent.pos().x(),QMouseEvent.pos().y()
        if y>self.highy:
            if self.is_active:
                self.is_active = False
                self.current_time = self.default_time
                self.repaint()
            else:
                self.is_active = True
                self.repaint()
        else:
            if self.is_active:return
            if self.taps:
                znak=self.taps//abs(self.taps)
            else:
                znak=1
            if abs(self.taps)>19:
                speed=120
            elif abs(self.taps)>9:
                speed=30
            elif abs(self.taps)>4:
                speed=5
            else:
                speed=1
            speed*=znak

            if x>self.centerx and(self.taps==abs(self.taps)):
                self.taps=-1
                speed=-1
            elif x<self.centerx and not(self.taps==abs(self.taps)):
                self.taps=1
                speed=1
            self.default_time+=speed
            if self.default_time<1:
                self.default_time=1
            self.current_time=self.default_time
            self.taps+=speed//abs(speed)

            o=open("settings.ini","w")
            o.write(str(self.default_time))
            o.close()
            self.repaint()







class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.generate_widgets()

    def generate_widgets(self):
        self.tomato = TomatoTimer(self)
        self.tomato.show()


def main():
    app = QApplication(argv)
    prog = TomatoTimer()

    app.exec()


if __name__ == "__main__":
    main()
