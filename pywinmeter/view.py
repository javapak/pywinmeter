# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 14:04:13 2022

@author: javapak
"""
#from PIL import ImageTk
#import tkinter as tk
#from tkinter import ttk
        
        
#class View(ttk.Frame):
    #def __init__(self, parent):
        #ttk.Frame.__init__(self, parent)
        #self.icons = []

    
    #def endpoint_slider(self, key):
     #       self.update_idletasks()
      #      ttk.Label(self, textvariable=key).pack()
       #     ttk.Scale(self, from_=0, to_=100).pack()
        #    print('weewoo')

            
    

#    def session_slider_and_image(self, index, name): #testing purposes currently...
 #       self.update_idletasks()
  #      self.icons[index] = ImageTk.PhotoImage(self.icons[index])
   #     ttk.Label(self, image = self.icons[index]).pack(side=tk.TOP)
    #    ttk.Label(self, text = name).pack()
     #   ttk.Scale(self, from_=0, to_=100).pack()

import sys
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from PIL import ImageQt
import ctypes

user32 = ctypes.windll.user32
w, h = user32.GetSystemMetrics(0)/3, user32.GetSystemMetrics(1)/3

from qt_material import apply_stylesheet

#class to create PySide6 main window instance

class View(QtWidgets.QWidget):
    icons = {}
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.setWindowFlag(QtCore.Qt.Window.FramelessWindowHint)
        self.setFixedSize(h, w)
          
        self.scroll_panel = QtWidgets.QWidget()
        self.scroll_panel_layout = QtWidgets.QVBoxLayout(self.scroll_panel)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_panel)

        # layout
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(15,15,15,15)
        self.mainLayout.addWidget(self.scroll_area)
        

        apply_stylesheet(self, theme='dark_red.xml')
    
    def endpoint_view(self, endpoint_name, id, signal_func):
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        label = QtWidgets.QLabel(text = "<b>" + endpoint_name + "</b>")
        slider.setObjectName(id)
        self.scroll_panel_layout.addWidget(label)
        slider.valueChanged.connect(lambda: signal_func(id, slider.value()))
        self.scroll_panel_layout.addWidget(slider)
    
    
    def session_slider_view(self, key, id, signal_func): #add slider widgets to main window.
        layout = QtWidgets.QHBoxLayout()
        icon = QtGui.QImage(self.icons.get(key).rgbSwapped())
        pixmap = QtGui.QPixmap().fromImage(icon)
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setObjectName(id)
        slider.valueChanged.connect(lambda: signal_func(id, slider.value()))
        layout.addWidget(slider)

        self.scroll_panel_layout.addLayout(layout)
    
        

    
        



                
        

