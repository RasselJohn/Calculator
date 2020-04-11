from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QGridLayout, QLCDNumber, QPushButton, QWidget)


class Calculator(QWidget):

    def __init__(self):
        super().__init__()

        self.digitStack = []
        # было ли нажато '='
        self.isEqual = False
        self.currentNumber = ''

        # настройка приложения
        self.setAppOptions()

    def setAppOptions(self):
        self.setWindowTitle("Cl!")
        self.setWindowIcon(QIcon("calculator.ico"))
        self.setMaximumSize(QSize(230, 200))
        self.setLcdDisplay()
        self.settingLayout()

    def setLcdDisplay(self):
        self.lcdDisplay = QLCDNumber(12)
        self.lcdDisplay.setSegmentStyle(QLCDNumber.Flat)
        self.lcdDisplay.setMinimumSize(150, 50)

    def settingLayout(self):
        layout = QGridLayout()
        layout.addWidget(self.lcdDisplay, 0, 0, 1, 4)
        layout.addWidget(self.createButton("CE"), 1, 3)

        calcButtons = [['7', '8', '9', '/'],
                       ['4', '5', '6', '*'],
                       ['1', '2', '3', '-'],
                       ['0', '.', '=', '+']
                       ]

        [layout.addWidget(self.createButton(calcButtons[i][j]), i + 2, j)
         for i in range(0, 4)
         for j in range(0, 4)]

        self.setLayout(layout)

    def createButton(self, buttonText):
        pb = QPushButton(buttonText)
        pb.setMinimumSize(40, 40)
        pb.clicked.connect(self.onButtonClick)
        return pb

    @pyqtSlot()
    def onButtonClick(self):
        self.handleButton(self.sender().text())

    def handleButton(self, pressedButtonText):
        if pressedButtonText == "CE":
            self.pressedCe()

        elif pressedButtonText == ".":
            self.pressedPoint()

        elif pressedButtonText == "=":
            self.pressedEqual()

        elif pressedButtonText.isdigit():
            self.pressedDigit(pressedButtonText)

            # если операция
        else:
            self.pressedOperation(pressedButtonText)

    def pressedCe(self, displayMessage='0'):
        self.isEqual = False
        self.digitStack.clear()
        self.currentNumber = ""
        self.lcdDisplay.display(displayMessage)

    def pressedPoint(self):
        # если было нажато "=" ранее
        self.checkPressEquil()

        self.currentNumber += '.' if self.currentNumber != "" else "0."
        self.lcdDisplay.display(self.currentNumber)

    def pressedEqual(self):
        self.isEqual = True
        if len(self.digitStack) < 2 or self.currentNumber == "":
            return
        self.makeReckoning()

    def pressedDigit(self, pressedButtonText):
        # если было нажато "=" ранее
        self.checkPressEquil()

        # в стеке не должно быть 2 числа подряд
        if len(self.digitStack) == 1 and self.currentNumber == "":
            self.digitStack.clear()

        # не более 12 цифр
        if len(self.currentNumber) >= 12:
            return

        self.currentNumber += pressedButtonText
        self.lcdDisplay.display(self.currentNumber)

    def pressedOperation(self, pressedButtonText):
        self.isEqual = False
        digitStackLength = len(self.digitStack)

        if digitStackLength == 0:
            if self.currentNumber != "":
                self.digitStack.append(self.currentNumber)
                self.digitStack.append(pressedButtonText)
                self.currentNumber = ""

        elif digitStackLength == 1:
            self.digitStack.append(pressedButtonText)

        elif digitStackLength == 2:
            if self.currentNumber != "":
                self.makeReckoning()
            else:
                self.digitStack.pop()

            self.digitStack.append(pressedButtonText)

    def calculate(self):
        rightNum = float(self.digitStack.pop())
        operation = self.digitStack.pop()
        leftNum = float(self.digitStack.pop())
        result = 0
        if operation == "+":
            result = leftNum + rightNum
        elif operation == "-":
            result = leftNum - rightNum
        elif operation == "/":
            result = leftNum / rightNum
        elif operation == "*":
            result = leftNum * rightNum
        return result

    def checkPressEquil(self):
        # если было нажато "=" ранее
        if self.isEqual:
            self.digitStack.clear()
            self.isEqual = False

    def makeReckoning(self):
        self.digitStack.append(self.currentNumber)
        rez = self.calculate()
        self.digitStack.clear()

        # для длинных значений
        if rez > 999999999999:
            self.pressedCe('Error!')
            return

        self.digitStack.append(str(rez))
        self.currentNumber = ""
        self.lcdDisplay.display(rez)
