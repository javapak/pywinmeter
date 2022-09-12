# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 14:04:13 2022

@author: javapak
"""
from PIL import ImageTk
import tkinter as tk
from tkinter import ttk
        
        
class View(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.icons = []

    
    def endpoint_slider(self, key):
            self.update_idletasks()
            ttk.Label(self, textvariable=key).pack()
            ttk.Scale(self, from_=0, to_=100).pack()
            print('weewoo')

            
    

    def session_slider_and_image(self, index, name): #testing purposes currently...
        self.update_idletasks()
        self.icons[index] = ImageTk.PhotoImage(self.icons[index])
        ttk.Label(self, image = self.icons[index]).pack(side=tk.TOP)
        ttk.Label(self, text = name).pack()
        ttk.Scale(self, from_=0, to_=100).pack()
                
                
        

