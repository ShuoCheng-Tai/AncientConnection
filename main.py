#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Title: main.py
#Version: AnncientConnection (1.0)
#Description: 
#Usage: 
#Input/Output: 
#Procedure: 
#Date­: 04/Mar/2024
#Author: Shuo-Cheng Tai (Leo)

####################################################################################################

# import os for set directory and path
import os
# import re for pattern to find matching files in a directory
import re
# import kivy and set the minimum version requirement 
import kivy
kivy.require('2.3.0')
## App module to create an App
from kivy.app import App
## Fixing window size for App window and Window background colour
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
# import modules for App window design
## Label for Grid names
from kivy.uix.label import Label
## Widget for Layout design in .kv file
from kivy.uix.widget import Widget
## BoxLayout, GridLayout, FloatLayout to set the layout of App window and button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
## DropDownm, Spinner, Button are modules to design the buttons
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
## ObjectProperty communicate .kv file with python script to set function of buttons
from kivy.properties import ObjectProperty


from kivy.uix.textinput import TextInput
from kivy.uix.image import Image



# Set the Directory and create Database
files = os.listdir("./TestUsers")

# Test user txt files
pattern = r"Test\d.txt"
tester = [file for file in files if re.match(pattern, file) and "DNA" not in file and file.endswith(".txt")]

# mtDNA Tree
mtDNA_data = {}
with open('./AncientMtDNA/mt_phyloTree_b17_Tree2.txt', 'r') as f:
    for line in f:
        names_mt = line.split()
        if len(names_mt) == 1 or "#" in names_mt:
            continue
        elif len(names_mt) == 2:
            mtDNA_data[names_mt[1]] = names_mt[0]

# Y DNA Tree
Y_DNA_data = {}
with open('./AncientYDNA/chrY_hGrpTree_isogg2016.txt', 'r') as f:
    for line in f:
        names_y = line.split()
        if len(names_y) == 1 or "#" in names_y:
            continue
        elif len(names_y) == 2:
            Y_DNA_data[names_y[1]] = names_y[0]



# Design & Script
class ACGrid(Widget):
    test2 = ObjectProperty(None)
    test1 = ObjectProperty(None)
    dna = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.test1.values = tester
        self.ids.test2.values = tester

    def btn(self):
        print("Selected values:")
        print("User 1:", self.test1.text)
        print("User 2:", self.test2.text)
        print("DNA:", self.dna.text)


# Execute the App
class AnncientConnectionApp(App):
    def build(self):
        Window.clearcolor = (.245, .245, .220, 0.5)
        return ACGrid()

if __name__ == "__main__":
    AnncientConnectionApp().run()
