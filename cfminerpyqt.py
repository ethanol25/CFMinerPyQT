import sys
import requests
import datetime
import random
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import *


## main starting window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
       
        self.uLabel = QLabel("Enter CF Username")
        self.rLabel = QLabel("Rating of Problem")
        self.nLabel = QLabel("Number of Problems")

        #enter username
        self.user = QLineEdit()

        #enter rating
        self.rating = QSpinBox()

        self.rating.setRange(800,3500)
        self.rating.setSingleStep(100)
        self.rating.lineEdit().setReadOnly(True)

        #enter number of problems
        self.numberOf = QSpinBox()

        self.numberOf.setRange(1,20)
        self.numberOf.lineEdit().setReadOnly(True)

        #enter button
        self.enter = QPushButton("Enter")
        self.enter.clicked.connect(self.enter_function)


        layout = QVBoxLayout()
        layout.addWidget(self.uLabel)
        layout.addWidget(self.user)
        layout.addWidget(self.rLabel)
        layout.addWidget(self.rating)
        layout.addWidget(self.nLabel)
        layout.addWidget(self.numberOf)
        layout.addWidget(self.enter)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def enter_function(self):
        print("clicked")
        self.get_random_problem()

    def get_random_problem(self):
        print("getting problem")
        url = 'https://codeforces.com/api/problemset.problems'

        try:
            response = requests.get(url)

            if response.status_code == 200:
                problemset = response.json()
                problems = []
                count = self.numberOf.value()

                for item in problemset["result"]["problems"]: 
                            if item.get("rating") == self.rating.value():
                                problems.append((item["contestId"], item["index"]))

                if count > len(problems):
                     count = len(problems)

                chosen = random.sample(problems, count)
                print(chosen)

                dlg = CustomDialog(chosen)
                dlg.exec()
            else:
                print("Error:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print('Error:', e)

    def check_completion(self):
        print("check completion")

class CustomDialog(QDialog):
     def __init__(self, problems):
        super().__init__()
        self.setWindowTitle("CF Problems")

        layout = QVBoxLayout()

        if not problems:
             layout.addWidget(QLabel("Error/No problems found"))
        else:
             for p in problems:
                contestId = p[0]
                problemIndex = p[1]

                url = f"https://codeforces.com/problemset/problem/{contestId}/{problemIndex}"
                
                linkText = f'<a href="{url}">Problem {contestId}{problemIndex}</a>'

                label = QLabel(linkText)
                label.setOpenExternalLinks(True)
                layout.addWidget(label)
        closeButton = QPushButton("Close")
        closeButton.clicked.connect(self.accept)
        layout.addWidget(closeButton)

        self.setLayout(layout)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

