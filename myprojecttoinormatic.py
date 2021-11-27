# coding: utf-8
"""Аналогично тому, как написание картины является искусством для души,
так и написание программы является искусством для разума."""

# импорты
import sys, random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QPushButton, QLabel, QStatusBar
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QPainter, QColor, QPen


class Tetromino(object):  # для рандома и очистки
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Shape(object):  # тетраминошки

    coordsShapes = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),  # нет ничего
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),  # Z
        ((0, -1), (0, 0), (1, 0), (1, 1)),  # S
        ((0, -1), (0, 0), (0, 1), (0, 2)),  # сосиська
        ((-1, 0), (0, 0), (1, 0), (0, 1)),  # Т
        ((0, 0), (1, 0), (0, 1), (1, 1)),  # кубик
        ((-1, -1), (0, -1), (0, 0), (0, 1)),  # Z но перевернутая
        ((1, -1), (0, -1), (0, 0), (0, 1))  # S но перевернутая
    )  # координаты для фигурок

    # чтобы понять, лучше нарисовать схему

    def __init__(self):
        self.coords = [[0, 0] for i in range(4)]  # делаем список координат
        self.pieceShape = Tetromino.NoShape  # как и мир начался с большого взрыва
        self.setShape(Tetromino.NoShape)  # так и игра начинается с пустоты

    def shape(self):
        return self.pieceShape  # фигачим фигуру

    def setShape(self, shape):  # размещение фигуры на столе
        table = Shape.coordsShapes[shape]

        for i in range(4):  # xy размещение
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape  # текущая , ничего не отобразится без этой штуки

    def setRandomShape(self):  # берем рандомную фигуру

        self.setShape(random.randint(1, 7))

    def x(self, index):  # х координата
        return self.coords[index][0]

    def y(self, index):  # у координата
        return self.coords[index][1]

    def setX(self, index, x):  # ставим координату, для переворота
        self.coords[index][0] = x

    def setY(self, index, y):  # ставим координату, для переворота
        self.coords[index][1] = y

    def minX(self):  # определяем максимум и минимум чтобы правильно позиционировать
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):  # определяем максимум и минимум чтобы правильно позиционировать
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):  # определяем максимум и минимум чтобы правильно позиционировать
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):  # определяем максимум и минимум чтобы правильно позиционировать
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotate(self):  # делаем поворот
        if self.pieceShape == Tetromino.SquareShape:  # квадратик неповоротливый
            return self

        res = Shape()  # ,ерем отдельный экземпляр
        res.pieceShape = self.pieceShape

        for i in range(4):  # разворот нвлево
            res.setX(i, self.y(i))
            res.setY(i, -self.x(i))

        return res


class MyMainWindow(QMainWindow):  # обьявление главного окна

    def __init__(self):  # инициализация
        super().__init__()
        self.widgets = []
        self.startPanel()  # по шаблону

    def startPanel(self):
        self.setWindowTitle('Tetris')  # название окна
        self.resize(560, 670)  # размер окна
        palette = QtGui.QPalette()  # ща будем красить окно, берем палитру
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))  # берем кисти
        brush.setStyle(QtCore.Qt.SolidPattern)  # специальные кисти!
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 255))  # макаем в краску
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.All, QtGui.QPalette.Window, brush)  # а шо мы красим?
        self.setPalette(palette)  # покрасили
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))  # красивенький курсор
        self.setTabShape(QtWidgets.QTabWidget.Rounded)  # я не помню зачем

        startButton = QPushButton('Start', self)  # кнопка старта
        startButton.setEnabled(True)
        startButton.setGeometry(QtCore.QRect(140, 220, 301, 111))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        startButton.setFont(font)
        startButton.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        startButton.setObjectName("startButton")
        startButton.clicked.connect(self.react_startbutton)

        quitButton = QPushButton('Quit', self)  # кнопка выхода
        quitButton.setGeometry(QtCore.QRect(220, 590, 141, 31))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        quitButton.setFont(font)
        quitButton.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        lbTetris = QLabel(self)  # та самая большая надпись Тетрис
        lbTetris.setGeometry(QtCore.QRect(120, 70, 430, 110))  # геометрия
        font = QtGui.QFont()  # шрифт
        font.setFamily("Arial")  # шрифт
        font.setPointSize(72)  # размер шрифта
        font.setBold(True)  # жирненький
        font.setWeight(75)  # тож размер
        lbTetris.setFont(font)  # установка шрифта
        lbTetris.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))  # красивый курсорчик
        lbTetris.setTextFormat(QtCore.Qt.PlainText)  # это явно что-то делает,
        # но после переработки кода из генератора потеряся смысл
        lbTetris.setText("Tetris")  # ну и собственно сам текст

        lbmadeby = QtWidgets.QLabel(self)  # моя авторская метка
        lbmadeby.setGeometry(QtCore.QRect(280, 180, 150, 20))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        lbmadeby.setFont(font)
        lbmadeby.setText("made by zuzuka28")

        self.show()
        self.widgets = [startButton, quitButton, lbTetris, lbmadeby]  # а это чтобы не мешали иконки

        quitButton.clicked.connect(QCoreApplication.instance().quit)  # выход по кнопке
        startButton.clicked.connect(self.react_startbutton)

    def react_startbutton(self):
        for w in self.widgets:  # мне приходится удалять все-все виджеты (
            w.deleteLater()
        # вернуться обратно к этому окну просто нереально

        self.main_widget = Board(self)  # установка главного виджета
        self.setCentralWidget(self.main_widget)

        self.statusbar = self.statusBar()  # статусбар
        self.main_widget.msg2Statusbar[str].connect(self.statusbar.showMessage)  # связываем действие и реакцию

        self.main_widget.start()  # начинаем игру


"""Люди считают, что программирование — это наука избранных,
но в реальности все наоборот — просто много людей создают программы,
которые используют чужие программы, как-будто строя стену из маленьких кирпичиков."""


class Board(QFrame):  # основное окно
    msg2Statusbar = pyqtSignal(str)  # связываем..

    BoardWidth = 12  # длина игрового поля
    BoardHeight = 18  # высота игрового поля
    Speed = 300  # скорости поля. ходят легенды что если ее изменить, играть будет в разы сложнее

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()  # инициализация по шаблону, ничего необычного

    def initBoard(self):
        self.timer = QBasicTimer()  # таймер. работает странно но работает
        self.isWaitingAfterLine = False

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0  # количество удаленных линий. проще - счет
        self.board = []  # доска это список координат

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False  # для старта и паузы игры
        self.isPaused = False
        self.clearBoard()

        """Некоторые проблемы лучше не решать, а избегать."""

        lbpaused = QtWidgets.QLabel(self)  # надпись Пауза
        lbpaused.setGeometry(QtCore.QRect(120, 70, 430, 110))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(72)
        font.setBold(True)
        font.setWeight(75)
        lbpaused.setFont(font)
        lbpaused.setText("Game Paused")
        lbpaused.hide()  # тут должно быть show но как блин всетаки это скрывать

        lbgameover = QtWidgets.QLabel(self)  # надпись Конец игры
        lbgameover.setGeometry(QtCore.QRect(50, 70, 460, 110))
        font = QtGui.QFont()  # шрифт
        font.setFamily("Arial")  # шрифт
        font.setPointSize(50)  # размер шрифта
        font.setBold(True)  # жирненький
        font.setWeight(75)
        lbgameover.setFont(font)
        lbgameover.setText("Game Over")
        lbgameover.hide()  # тут должно быть show но как блин всетаки это скрывать
        self.pauseover = [lbpaused, lbgameover]

    def shapeAt(self, x, y):  # cпавним фигуру
        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):  # спавним фигуру
        self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):  # размер кубика, но если менять размер окна, он уже не кубик..
        return self.contentsRect().width() // Board.BoardWidth

    def squareHeight(self):  # размер кубика, но если менять размер окна, он уже не кубик..
        return self.contentsRect().height() // Board.BoardHeight

    def start(self):  # старт игры
        if self.isPaused:  # если на паузе
            return

        self.isStarted = True  # параметр для нормальной паузы
        self.isWaitingAfterLine = False  # для смещения по линии
        self.numLinesRemoved = 0  # cчетчик убраных линий
        self.clearBoard()  # очистка доски

        self.msg2Statusbar.emit(str(self.numLinesRemoved))  # вывод убраных линий

        self.newPiece()  # новая фигура
        self.timer.start(Board.Speed, self)  # счетчик для падения

    def pause(self):  # пауза

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused  # клацаем паузу

        if self.isPaused:  # еcли на паузе -- тормозим линии и выводим в статусбар
            self.timer.stop()
            self.msg2Statusbar.emit("paused")
            # self.pauseover[0].show()
            # боже как заставить работать эти лейблы я не понимаю я уже так намучался

        else:
            self.timer.start(Board.Speed, self)  # иначе же снимаем с паузы
            self.msg2Statusbar.emit(str(self.numLinesRemoved))
            # self.pauseover[0].hide()
            # боже как заставить работать эти лейблы я не понимаю я уже так намучался

        self.update()  # обновим для корректной работы

    def paintEvent(self, event):  # это и занимается отрисовкой
        painter = QPainter(self)  # в этой библиотеке очень интересный механизм отрисовки.
        # почему-то пример моего изначального старания как-то низкоуровнево устроен..
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)

                if shape != Tetromino.NoShape:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetromino.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                                boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),
                                self.curPiece.shape())

    def keyPressEvent(self, event):
        if not self.isStarted or self.curPiece.shape() == Tetromino.NoShape:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotate(), self.curX, self.curY)

        elif key == Qt.Key_Space:
            self.dropDown()

        elif key == Qt.Key_Down:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()
        else:
            super(Board, self).timerEvent(event)

    def clearBoard(self):
        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetromino.NoShape)

    def dropDown(self):
        newY = self.curY
        while newY > 0:

            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break

            newY -= 1

        self.pieceDropped()

    def oneLineDown(self):  # спускаемся вниз постепенно
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()

    def pieceDropped(self):  # спускаемся вниз одним движением
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()

    def removeFullLines(self):  # удаление заполненных линий
        numFullLines = 0
        rowsToRemove = []

        # ну проходимся и ищем заполненную линию, заполняем ее пустой фигурой и смещаем вниз все

        for i in range(Board.BoardHeight):
            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetromino.NoShape:
                    n = n + 1
            if n == 12:  # своеобразный костыль. при изменении размера поля количество кубиков не меняется
                rowsToRemove.append(i)

        rowsToRemove.reverse()

        for m in rowsToRemove:
            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                    self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:
            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetromino.NoShape)
            self.update()

    """ Программирование — это как бить себя по лицу: рано или поздно ваш нос будет кровоточить."""

    def newPiece(self):
        self.curPiece = Shape()
        self.curPiece.setRandomShape()
        self.curX = Board.BoardWidth // 2 + 1  # спавним по середине
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):
            self.curPiece.setShape(Tetromino.NoShape)
            self.timer.stop()
            self.isStarted = False
            self.msg2Statusbar.emit("Loser")
            self.pauseover[1].show()
            # я крайне шокирован тем что это работает а пауза нет

    def tryMove(self, newPiece, newX, newY):
        for i in range(4):
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False

            if self.shapeAt(x, y) != Tetromino.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()
        return True

    def drawSquare(self, painter, x, y, shape):
        colors = (0x000000,  # красивая зеленая палитра
                  0x00FF7F,
                  0x3CB371,
                  0x2E8B57,
                  0x228B22,
                  0x008000,
                  0x006400,
                  0x9ACD32)

        # покраска блоков

        color = QColor(colors[shape])

        painter.fillRect(x + 1, y + 1,
                         self.squareWidth() - 2,
                         self.squareHeight() - 2,
                         color)

        painter.setPen(color.lighter())

        painter.drawLine(x, y + self.squareHeight() - 1,
                         x, y)
        painter.drawLine(x, y,
                         x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())

        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + 1)


"""Всегда пишите код так, будто сопровождать его будет 
склонный к насилию психопат, который знает, где вы живете."""

app = QApplication(sys.argv)  # приложение
tetris = MyMainWindow()
sys.exit(app.exec_())  # норм выход