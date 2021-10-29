import random
import os
import sys
from sys import argv, executable
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QApplication, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QFont


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.wrong_letters = []
        self.right_letters = 0
        self.letter = ''
        self.flag = False
        self.word = 'a'
        self.language = ''
        self.level = ''
        self.flag2 = False
        

    def initUI(self):
        self.list_of_buttons = []
        self.list_of_labels = []

        self.again = QPushButton('ЗАНОВО', self)
        self.again.setStyleSheet("QPushButton:!hover { color: #ffffff; background: #000063 }")
        self.again.resize(130, 75)
        self.again.move(1700, 70)
        self.again.clicked.connect(self.onClicked1)
        self.again.hide()

        font1 = QtGui.QFont()
        font1.setPointSize(35)
        font1.setFamily('Mistral')

        self.label_gallows = QLabel(self)
        self.label_gallows.setText('В И С Е Л И Ц А')
        self.label_gallows.move(680, 255)
        self.label_gallows.setFont(font1)
        self.label_gallows.setStyleSheet('color: rgb(51, 0, 153)')
        
        self.label_looser = QLabel(self)
        self.label_looser.setText('Вы проиграли')
        self.label_looser.move(520, 345)  
        self.label_looser.setFont(font1)
        self.label_looser.setStyleSheet('color: rgb(51, 0, 153)')
        self.label_looser.hide()
        
        font1.setPointSize(47)
        self.label_winner = QLabel(self)
        self.label_winner.setText('Вы выиграли!')
        self.label_winner.move(780, 355)  
        self.label_winner.setFont(font1)
        self.label_winner.setStyleSheet('color: rgb(51, 0, 153)')
        self.label_winner.hide()
        
        font = QtGui.QFont()
        font.setPointSize(10)
        self.but_russian = QPushButton('Русский', self)
        self.but_russian.resize(130, 75)
        self.but_russian.move(800, 400) 
        self.but_russian.setFont(font)
        self.but_russian.clicked.connect(self.onClickedLang)
        self.but_russian.setStyleSheet("QPushButton:!hover { color: #ffffff; background: #000063 }")

        self.but_english = QPushButton('Английский', self)
        self.but_english.resize(130, 75)
        self.but_english.move(800, 500)
        self.but_english.setFont(font)
        self.but_english.clicked.connect(self.onClickedLang)
        self.but_english.setStyleSheet("QPushButton:!hover { color: #ffffff; background: #000063 }")        

        self.but_easy = QPushButton('Легкий', self)
        self.but_easy.setStyleSheet("QPushButton:!hover { color: #ffffff; background: #000063 }")
        self.but_easy.resize(130, 75)
        self.but_easy.move(800, 300)
        self.but_easy.hide()
        self.but_easy.clicked.connect(self.onClickedDiff)

        self.but_medium = QPushButton('Средний', self)
        self.but_medium.setStyleSheet("QPushButton:!hover { color: #ffffff; background: #000063 }")
        self.but_medium.resize(130, 75)
        self.but_medium.move(800, 400)
        self.but_medium.hide()
        self.but_medium.clicked.connect(self.onClickedDiff)

        self.but_hard = QPushButton('Сложный', self)
        self.but_hard.setStyleSheet("QPushButton:!hover { color: #ffffff; background: #000063 }")
        self.but_hard.resize(130, 75)
        self.but_hard.move(800, 500)
        self.but_hard.hide()
        self.but_hard.clicked.connect(self.onClickedDiff)

        self.update()
        self.setGeometry(0, 0, 10000, 10000)
        self.setWindowTitle('Виселица')
        self.show()

    def onClickedLang(self):
        self.label_gallows.hide()
        self.language = self.sender().text()
        self.but_easy.show() 
        self.but_medium.show() 
        self.but_hard.show()  
        self.but_russian.hide()
        self.but_english.hide()

    def onClickedDiff(self):
        self.level = self.sender().text()
        self.again.show()
        self.but_easy.hide()
        self.but_medium.hide()
        self.but_hard.hide()
        self.flag = True
        self.update()
        self.initLetters()

        for button in self.list_of_buttons:
            button.show()

    def setWord(self, file):
        with open(file, encoding='utf-8') as f:
            text = f.read()
            words = text.split()
            good_words = []
            for each in words:
                if 6 < len(each) < 13:
                    good_words.append(each)
            self.word = random.choice(good_words)
    
    def addLetters(self, letters):
        self.list_of_labels = []
        positions = [620, 720, 820, 920, 1020, 1120, 1220, 1320, 1420, 1520, 1620]
        font2 = QtGui.QFont()
        font2.setPointSize(22)
        font2.setFamily('Mistral')

        list_dict = []
        
        for list_let in letters:
            list_dict.append(dict(zip(list_let, positions)))

        for i in range(len(list_dict)):
            for letter1, position1 in list_dict[i].items():
                but = QPushButton(letter1, self)    
                but.move(position1, 650 + i*100)
                but.resize(65, 65)
                but.clicked.connect(self.onClicked1)
                but.setStyleSheet("color: rgb(51, 0, 153); background-color: rgba(255, 255, 255, 0);")
                but.setFont(font2)
                self.list_of_buttons.append(but)
                but.hide()

    def initLetters(self):
        if self.language == 'Русский':
            self.setWord('words_rus.txt')
            letters = [['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й'],
                        ['К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф'],
                        ['Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']]
            self.addLetters(letters)
        if self.language == 'Английский':
            self.setWord('words_eng.txt')
            letters = [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
                        ['L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V'],
                        ['W', 'X', 'Y', 'Z']]
            self.addLetters(letters)
        
        
        x = 1010 
        for let in self.word:
            font3 = QtGui.QFont()
            font3.setPointSize(15)
            font3.setFamily('Mistral')
            label = QLabel(self)
            label.setText(let.upper())
            label.move(x, 370)  
            label.setFont(font3)
            label.setStyleSheet('color: rgb(51, 0, 153)')
            label.hide() 
            x += 50 
            self.list_of_labels.append(label)


    def restart1(self):
        os.execl(executable, os.path.abspath(__file__), *argv)

    def onClicked1(self):
        if self.sender().text() == 'ЗАНОВО':
            self.restart1()	
        self.letter = self.sender().text().lower()

        if self.letter not in self.word and self.flag2 == False:
            self.update()

        counted_letters = self.word.count(self.sender().text().lower())
        self.right_letters += counted_letters
        for label in self.list_of_labels:
            if self.sender().text() == label.text():
                label.show()

        for button in self.list_of_buttons:
            if self.letter.upper() == button.text():
                button.hide()
        
        if len(self.word) == self.right_letters:
            self.label_winner.show()
        errors = 16
        if self.level == 'Легкий':
            errors -= 1
        if self.level == 'Средний':
            errors -= 4
        if self.level == 'Сложный':
            errors -= 7

        if len(self.wrong_letters) == errors or len(self.word) == self.right_letters:
            self.flag2 = True
            self.update()
            for button in self.list_of_buttons:
                button.hide()
            for label in self.list_of_labels:
                label.hide()
            
        if len(self.wrong_letters) == errors:
            self.label_looser.show()
            for label in self.list_of_labels:
                if label.text().lower() in self.word:
                    label.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        self.draw_background(qp)
        if len(self.word) != self.right_letters and self.flag:
            self.draw_lines(qp)

        if self.flag2 == False:
            if self.letter != 'заново' and len(self.wrong_letters) == 0 and self.letter not in self.wrong_letters and self.letter or len(self.wrong_letters) >= 1:
                self.draw_gallows_column(qp)

            if self.level == 'Легкий':
                if len(self.wrong_letters) >= 1:
                    self.draw_gallows_lower_part1(qp)

                if len(self.wrong_letters) >= 2:
                    self.draw_gallows_lower_part2(qp)

                if len(self.wrong_letters) >= 3:
                    self.draw_gallows_lower_part3(qp)

                if len(self.wrong_letters) >= 4:
                    self.draw_gallows_upper_part(qp)

                if len(self.wrong_letters) >= 5:
                    self.draw_gallows_upper_part2(qp)

                if len(self.wrong_letters) >= 6:
                    self.draw_rope(qp)

                if len(self.wrong_letters) >= 7:
                    self.draw_head(qp)

                if len(self.wrong_letters) >= 8:
                    self.draw_body(qp)

                if len(self.wrong_letters) >= 9:
                    self.draw_left_hand(qp)

                if len(self.wrong_letters) >= 10:
                    self.draw_right_hand(qp)

                if len(self.wrong_letters) >= 11:
                    self.draw_left_leg(qp)

                if len(self.wrong_letters) >= 12:
                    self.draw_right_leg(qp)

                if len(self.wrong_letters) >= 13:
                    self.draw_face(qp)

                if len(self.wrong_letters) >= 14:
                    self.draw_hair(qp)

                if len(self.wrong_letters) >= 15:
                    self.draw_bow_tie(qp)

            if self.level == 'Средний':
                if len(self.wrong_letters) >= 1:
                    self.draw_gallows_lower_part1(qp)

                if len(self.wrong_letters) >= 2:
                    self.draw_gallows_upper_part(qp)

                if len(self.wrong_letters) >= 3:
                    self.draw_gallows_upper_part2(qp)

                if len(self.wrong_letters) >= 4:
                    self.draw_rope(qp) 

                if len(self.wrong_letters) >= 5:
                    self.draw_head(qp)

                if len(self.wrong_letters) >= 6:
                    self.draw_body(qp)

                if len(self.wrong_letters) >= 7:
                    self.draw_left_hand(qp)

                if len(self.wrong_letters) >= 8:
                    self.draw_right_hand(qp)

                if len(self.wrong_letters) >= 9:
                    self.draw_left_leg(qp)

                if len(self.wrong_letters) >= 10:
                    self.draw_right_leg(qp)

                if len(self.wrong_letters) >= 11:
                    self.draw_face(qp)

                if len(self.wrong_letters) >= 12:
                    self.draw_hair(qp)

            if self.level == 'Сложный':
                if len(self.wrong_letters) >= 1:
                    self.draw_gallows_upper_part(qp)

                if len(self.wrong_letters) >= 2:
                    self.draw_rope(qp) 

                if len(self.wrong_letters) >= 3:
                    self.draw_head(qp)

                if len(self.wrong_letters) >= 4:
                    self.draw_body(qp)

                if len(self.wrong_letters) >= 5:
                    self.draw_left_hand(qp)

                if len(self.wrong_letters) >= 6:
                    self.draw_right_hand(qp)

                if len(self.wrong_letters) >= 7:
                    self.draw_left_leg(qp)

                if len(self.wrong_letters) >= 8:
                    self.draw_right_leg(qp)

                if len(self.wrong_letters) >= 9:
                    self.draw_face(qp)  
            
            if self.letter not in self.word and self.letter not in self.wrong_letters:
                self.wrong_letters.append(self.letter)              
        qp.end()
    
    def draw_background(self,qp):
        pen = QPen(Qt.white, 4, Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(Qt.white)
        qp.drawRect(0, 0, 10000, 10000)
        pen3 = QPen(Qt.blue, 1, Qt.SolidLine)
        col = QColor(0, 0, 0)
        col.setNamedColor('#74a9f9')
        qp.setPen(col)
        y = 0
        while y < 2000:
            y += 30
            qp.drawLine(0, y, 2000, y)
        x = 0
        while x < 2000:
            x += 30
            qp.drawLine(x, 0, x, 2000)      


    def draw_lines(self, qp):
        col = QColor(51, 0, 153)
        self.pen = QPen(col, 4, Qt.SolidLine)
        self.pen2 = QPen(col, 4, Qt.DashDotDotLine)
        self.pen3 = QPen(col, 2, Qt.SolidLine)
        qp.setPen(self.pen)

        for i in range(len(self.word)):
            qp.drawLine(1000 + i*50, 400, 1030 + i*50, 400)

    def draw_gallows_column(self, qp):
        qp.drawLine(350, 90, 350, 610)

    def draw_gallows_lower_part1(self, qp):
        qp.drawLine(180, 610, 520, 610)
        qp.drawLine(350, 90, 350, 610)

    def draw_gallows_lower_part2(self, qp):
        qp.drawLine(350, 550, 520, 610)

    def draw_gallows_lower_part3(self, qp):
        qp.drawLine(180, 610, 350, 550)

    def draw_gallows_upper_part(self, qp):
        qp.drawLine(350, 90, 600, 90)

    def draw_gallows_upper_part2(self, qp):
        qp.drawLine(420, 90, 350, 160)

    def draw_rope(self, qp):
        qp.setPen(self.pen2)
        qp.drawLine(600, 90, 600, 215)

    def draw_head(self, qp):
        qp.setPen(self.pen)
        qp.drawEllipse(550, 210, 60, 60)

    def draw_body(self, qp):
        qp.drawLine(580, 270, 620, 270)
        qp.drawLine(580, 270, 570, 350)
        qp.drawLine(620, 270, 630, 350)
        qp.drawLine(630, 350, 570, 350)

    def draw_left_hand(self, qp):
        qp.drawLine(580, 270, 560, 320)
        qp.drawLine(560, 320, 560, 380)

    def draw_right_hand(self, qp):
        qp.drawLine(620, 270, 640, 315)
        qp.drawLine(640, 315, 640, 370)

    def draw_left_leg(self, qp):
        qp.drawLine(580, 350, 580, 430)
        qp.drawLine(580, 430, 565, 450)

    def draw_right_leg(self, qp):
        qp.drawLine(610, 350, 610, 390)
        qp.drawLine(610, 390, 615, 425)
        qp.drawLine(615, 425, 605, 445)

    def draw_hair(self, qp):
        qp.setPen(self.pen)
        qp.drawLine(560, 215, 535, 220)
        qp.drawLine(560, 215, 540, 235)
        qp.drawLine(560, 215, 570, 222)
        qp.drawLine(560, 215, 560, 224)
        qp.drawLine(560, 215, 580, 200)
        qp.drawLine(560, 215, 575, 190)
        qp.drawLine(560, 215, 560, 200)
        qp.drawLine(560, 215, 585, 215)
        qp.drawLine(560, 215, 546, 198)

    def draw_bow_tie(self, qp):
        qp.setPen(self.pen3)
        qp.drawLine(615, 255, 585, 290)
        qp.drawLine(580, 267, 620, 280)
        qp.drawLine(615, 255, 620, 280)
        qp.drawLine(580, 267, 585, 290)

    def draw_face(self, qp):
        qp.setPen(self.pen3)
        qp.drawLine(560, 240, 572, 241)
        qp.drawLine(564, 235, 568, 247)
        qp.drawLine(580, 224, 591, 230)
        qp.drawLine(585, 235, 588, 221)
        qp.drawArc(580, 245, 30, 30, 120 * 10, 160 * 10)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())