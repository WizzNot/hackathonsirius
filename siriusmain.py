import sys
from PyQt5 import QtCore, QtMultimedia
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMainWindow, QFileDialog
import pickle
import csv


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('hackathon.ui', self)
        self.resultbutton.clicked.connect(self.resultf)
        self.metikbutton.clicked.connect(self.me)
        self.clf = pickle.load(open('hackathon.pk1', 'rb'))
        self.setWindowTitle('Sirius')
        
    def resultf(self):
        a = [int(i) for i in self.lineEdit.text().replace(' ', '').split(',')]
        self.res.setText("".join([str(i) for i in self.clf.predict([a])]))
        
    def me(self):
        c = []
        a = QFileDialog.getOpenFileName()[0]
        with open(a, encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for i in reader:
                if any([j == 'Data' for j in i]):
                    g = i.index('Data')
                    break
            for i in reader:
                if 'Data' in i:
                    continue
                b = [int(j) for j in i[g].lstrip('"[').rstrip(']"').split(', ')]
                c.append(b)
        c = self.clf.predict(c)
        with open('answer.csv', 'w+', newline='', encoding="utf8") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            k = 0
            writer.writerow(['id', 'Class'])
            for i in c:
                writer.writerow([str(k), str(i)])
                k += 1
        self.metrika.setText("Успешно")


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
