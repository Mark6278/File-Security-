#! /bin/env python3

import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from base64 import *
from hashlib import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import *

class Main(QMainWindow):
   def __init__(self):
      super(Main, self).__init__(parent = None)
      self.setWindowTitle(" File security")
      self.setWindowIcon(QIcon("passicon.jpg"))
      self.setGeometry(450, 550, 450, 550)
      center = QWidget()
      self.setCentralWidget(center)
      cen = QGridLayout(center)
      back = QPushButton(self)
      back.resize(430, 530)
      back.setStyleSheet("border-image: url(passback.jpg);")
      cen.addWidget(back, 0, 0)
      change = QStackedWidget(self)
      cen.addWidget(change, 1, 0)
      main = QWidget()
      m = QGridLayout(main)
      self.option = QComboBox(main)
      self.option.addItems([ " Set password", " Remove password" ])
      m.addWidget(self.option, 0, 1)
      self.sF = QLineEdit(main)
      self.sF.setPlaceholderText(" File path")
      m.addWidget(self.sF, 1, 1)
      search = QPushButton("search", main)
      search.clicked.connect(self.secure_file)
      m.addWidget(search, 2, 1)
      self.ab = QPushButton("about", main)
      self.ab.setCheckable(True)
      self.ab.clicked.connect(self.about)
      m.addWidget(self.ab, 2, 3)
      self.Atxt = QLabel(main)
      m.addWidget(self.Atxt, 0, 3)
      sett = QPushButton("setting", main)
      sett.clicked.connect(lambda: change.setCurrentWidget(1))
      m.addWidget(sett, 1, 5)
      setting = QWidget()
      Sett = QGridLayout(setting)
      B = QPushButton("<", setting)
      Sett.addWidget(B, 0, 1)
      t1 = QLabel("file's source", setting)
      Sett.addWidget(t1, 0, 3)
      self.Sf = QComboBox(setting)
      self.Sf.addItems([ " sh   Shellscript", " py   Python" ])
      Sett.addWidget(self.Sf, 1, 4)
      t2 = QLabel("Theme", setting)
      Sett.addWidget(t2, 0, 6)
      self.Light = QRadioButton("  light", setting)
      self.Light.setChecked(True)
      self.Light.clicked.connect(self.light)
      Sett.addWidget(self.Light, 1, 7)
      self.Dark = QRadioButton("  Dark", setting)
      self.Dark.clicked.connect(self.dark)
      Sett.addWidget(self.Dark, 1, 8)
      self.time = QTimer(self)
      self.time.start(1800)

   def secure_file(self):
      if self.option.isCurrentText() == " Set password":
         self.file, check = QFileDialog.getOpenFileName(self, " File security", str(self.setP.text()), f"{self.sF.currentText()[8:]} files *.{self.sF.currentText()[1:8]}")
         try:
            if not self.file:
               return
         except FileNotFoundError:
               return
         with open(self.file, "r") as file:
            file.seek(12)
            self.rF = file.read()
         if "f" in self.rF:
            QMessageBox.warning(self, "Warning", "File already secured")
         else:
            self.setP = QDockWidget(self)
            self.setP.resize(300, 100)
            self.setP.setFeature(QDockWidget.Close)
            w = QWidget()
            self.lW = QGridLayout(w)
            self.lW.setConstentMargins(6, 6, 30, 0)
            self.passd = QLineEdit(w)
            self.passd.setPlaceholderText(" Creat password")
            self.lW.addWidget(self.passd, 0, 0)
            self.show_hide = QPushButton(w)
            self.show_hide.resize(15, 15)
            self.lW.addWidget(self.show_hide, 1, 0)
            self.eN = QPushButton(w, "Ok")
            self.eN.clicked.connect(self.enc)
            self.lW.addWidget(self.eN, 1, 1)
            self.war = QLabel(w, "Enter more then 5 digits")
            self.addDockWidget(QDockWidget.LeftDockWidgetArea, self.setP)
      else:
         self._file ,check = QFileDialog.getOpenFileName(self, " File security", str(self.setP.text()), f"{self.sF.currentText()[:8]} files *.{self.sF.currentText()[1:8]}")
         try:
            if not self.file:
               return
         except FileNotFoundError:
            return
         rF = open(self.file, "r").read()
         if "f" not in rF:
            QMessageBox.warning(self, "Warning", "File already not secured")
         else:
            self.remP = QDockWidget(self)
            self.setP.resize(300, 100)
            self.remtP.setFeature(QDockWidget.Close)
            w = QWidget()
            self.Lw = QGridLayout(w)
            self.Lw.setConstentMargins(6, 6, 30, 0)
            self.passwd = QLineEdit(w)
            self.passwd.setPlaceholderText(" Enter password")
            self.Lw.addWidget(self.passwd, 0, 0)
            self.show_hid = QPushButton(w)
            self.show_hid.resize(15, 15)
            self.Lw.addWidget(self.show_hid, 1, 0)
            self.En = QPushButton(w, "Ok")
            self.En.clicked.connect(self.dec)
            self.Lw.addWidget(self.En, 1, 1)
            self.War = QLabel(w, "Wrong")
            self.addDockWidget(QDockWidget.LeftDockWidgetArea, self.remP)

   def enc(self):
      if len(self.passd.text()) < 5:
         self.lW.addWidget(self.war)
         self.time.timeout.connect(lambda: self.war.setText(""))
      else:
         cipher = AES.new(self.key, AES.MODE_CBC)
         with open("y", "ab") as Pf, open("q", "ab") as If:
             Pf.write(self.file) + Pf.write(b":") + Pf.write(cipher.encrypt(pad(b64encode(self.passd.text()), AES.block_size)))
             If.wtite(self.file) + If.write(b":") + If.write(b64encode(cipher.iv))
         open(self.file, "a").write(open(self.file, "r").read().replace("#! /bin/bash", "#! /bin/bash\n\nf"))

   def dec(self):
      with open("y", "rb") as Pf, open("q", "rb") as If:
          for line in Pf:
             if os.path.basename(self._file) in line:
                pass_hash = line.split(b":")[1].strip(b"\n")
          for line_ in If:
             if os.path.basename(self._file) in line_:
                cipher = AES.new(self.key, AES.MODE_CBC, line_.split(b":")[1].strip(b"\n"))
          if self.passwd.text() != unpad(cipher.decrypt(b64decode(pass_hash))):
              self.Lw.addWidget(self.War, 0, 1)
              self.time.timeout.connect(lambda: self.War.setText(""))
          else:
          	with open("y", "rb+") as iF, open("q", "rb+") as pF:
          	content = iF.read()
              for __line in content:
              	if os.path.basename(self._file) in __line:
              
              contents = pF.read()
              for line__ in contents:
              	if os.path.basename(self._file):

   def light(self):
      self.setStyleSheet("""Main, QDockWidget, QMessageBox { background-color: gray;}
                            QLineEdit { border: 0; border-bottom: 2px solid black; font: bold;}
                            QComboBox { border-radius: 10px;}""")

   def dark(self):
      self.setStyleSheet("""Main, QDockWidget, QMessageBox { background-color: black;}
                            QLineEdit { border: 0; border-bottom: 2px solid cyan; color: white; font: bold;}
                            QComboBox { border-radius: 10px;}""")

   def about(self):
      if self.ab.isChecked(True):
         self.Atxt.setText("This is a app")
      else:
         self.Atxt.setText("")


app = QApplication([])
w = Main()
w.show()
app.exec()
