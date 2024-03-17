import json
import pygame

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from main import main_game

app = QApplication([])
app.setStyleSheet(
"""

""")
settings = {}
def read_data():
    global settings
    with open("settings.json", "r", encoding="utf-8") as file:
        settings = json.load(file)
def write_data():
    global settings
    with open("settings.json", "w", encoding="utf-8") as file:
        json.dump(settings, file)
window = QWidget()


read_data()
print(settings)

start_btn = QPushButton("Старт")
title = QLabel("Tetris")

main_line = QVBoxLayout()
main_line.addWidget(title)
main_line.addWidget(start_btn)

window.setLayout(main_line)

start_btn.clicked.connect(main_game)

window.show()
app.exec()