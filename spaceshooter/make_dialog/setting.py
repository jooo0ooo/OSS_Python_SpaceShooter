# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from os import path
import os
import subprocess
import easygui

img_dir = path.join(path.dirname(__file__), '../assets')

class MySetting(QMainWindow):
    def __init__(self):
        super().__init__()
        self.background_image= QLabel(self)
        self.background_image.resize(700,310)
        background_pixmap = QPixmap(path.join(img_dir,'setting_menu.jpg'))
        self.background_image.setPixmap(background_pixmap)

        #저장버튼
        Save_btn = QPushButton("Start", self)
        Save_btn.setStyleSheet("background-color:black; color:#586591;")
        Save_btn.resize(80,30)
        Save_btn.move(500,250)

        #레벨난이도 체크박스
        self.Level_combobox = QComboBox(self)
        self.Level_combobox.setStyleSheet("background-color:black;color:#586591;font-size:13pt;")
        self.Level_combobox.addItem("Level1")
        self.Level_combobox.addItem("Level2")
        self.Level_combobox.addItem("Level3")
        self.Level_combobox.addItem("Level4")
        self.Level_combobox.addItem("Level5")
        self.Level_combobox.move(620,100)
        self.Level_combobox.resize(80, 30)
        #종료버튼
        Exit_btn=QPushButton("Exit", self)
        Exit_btn.resize(80,30)
        Exit_btn.setStyleSheet("background-color:black; color:#586591;")
        Exit_btn.move(600,250)

        #기체색깔 콤보박스

        self.Player1_Color_combobox = QComboBox(self)
        self.Player1_Color_combobox.setStyleSheet("background-color:black;color:#586591;font-size:13pt;")
        self.Player1_Color_combobox.addItem("RED")
        self.Player1_Color_combobox.addItem("BLUE")
        self.Player1_Color_combobox.addItem("ORANGE")
        self.Player1_Color_combobox.addItem("PINK")
        self.Player1_Color_combobox.addItem("YELLOW")
        self.Player1_Color_combobox.addItem("GOLD")
        self.Player1_Color_combobox.addItem("PURPLE")
        self.Player1_Color_combobox.move(520,190)
        self.Player1_Color_combobox.resize(80,30)




        self.Player2_Color_combobox = QComboBox(self)
        self.Player2_Color_combobox.setStyleSheet("background-color:black;color:#586591;font-size:13pt;")
        self.Player2_Color_combobox.addItem("RED")
        self.Player2_Color_combobox.addItem("BLUE")
        self.Player2_Color_combobox.addItem("ORANGE")
        self.Player2_Color_combobox.addItem("PINK")
        self.Player2_Color_combobox.addItem("YELLOW")
        self.Player2_Color_combobox.addItem("GOLD")
        self.Player2_Color_combobox.addItem("PURPLE")
        self.Player2_Color_combobox.move(620,190)
        self.Player2_Color_combobox.resize(80,30)

        Exit_btn.clicked.connect(self.Exit_clicked)
        Save_btn.clicked.connect(self.Save_clicked)
        self.setGeometry(500, 300, 700, 310) #setGeometry(x축,y축,가로길이,세로길이)
        self.setFixedSize(700,310)
        self.setWindowTitle('Setting')
        self.show()

    def Save_clicked(self):
        Setting_text_file = open("setting.txt","w",encoding="utf-8")


        Selected_level = self.Level_combobox.currentText()
        Player1_Selected_Color = self.Player1_Color_combobox.currentText()
        Player2_Selected_Color = self.Player2_Color_combobox.currentText()

        print("레벨은 ",Selected_level)
        print("P1 비행기 색깔은 ", Player1_Selected_Color)
        print("P2 비행기 색깔은 ",Player2_Selected_Color)
        temp = "Selected_Level="+Selected_level+" P1_Selected_Color="+Player1_Selected_Color+" P2_Selected_Color="+Player2_Selected_Color
        Setting_text_file.write(temp)

        Setting_text_file.close()
        subprocess.call(['python3', '../spaceShooter.py'])
        #sys.exit()





    def Exit_clicked(self):
        sys.exit()

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MySetting()
    sys.exit(app.exec_())
