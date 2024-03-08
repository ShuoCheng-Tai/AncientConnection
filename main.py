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
from kivy.uix.popup import Popup

# Module for excel .xlsx file type
import pandas as pd

# For creating plots
#from kivy.garden.graph import Graph, MeshLinePlot

#
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

####################################################################################################

# Set the Directory and create Database
main_directory = os.getcwd()
files = os.listdir("./TestUsers")

## Test user txt files
pattern = r"Test\d.txt" 
tester_file = sorted([file for file in files if re.match(pattern, file) and "DNA" not in file and file.endswith(".txt")])
tester_name = [os.path.splitext(file)[0] for file in tester_file]
## Assign names to files and store in a dictionary
tester_library = {name: file for name, file in zip(tester_name, tester_file)}

# mtDNA Tree
mtDNA_data = {}
with open('./AncientMtDNA/mt_phyloTree_b17_Tree2.txt', 'r') as f:
    for line in f:
        names_mt = line.split()
        if len(names_mt) == 1 or "#" in names_mt:
            continue
        elif len(names_mt) == 2:
            mtDNA_data[names_mt[0]] = names_mt[1]

# Y DNA Tree
Y_DNA_data = {}
with open('./AncientYDNA/chrY_hGrpTree_isogg2016.txt', 'r') as f:
    for line in f:
        names_y = line.split()
        if len(names_y) == 1 or "#" in names_y:
            continue
        elif len(names_y) == 2:
            Y_DNA_data[names_y[0]] = names_y[1]


# Extract data from Excel sheet
df = pd.read_excel('./AADR_54.1/AADR Annotation.xlsx')
excel_mt_id_col = df.iloc[:,28]
excel_y_id_col = df.iloc[:,[25,26]]

#print(excel_mt_id_col.head(5))
#print(excel_y_id_col.head(5))
####################################################################################################

# Define Functions

def find_ancestors(node,tree):
    ancestors = []
    while node:
        ancestors.append(node)
        node = tree.get(node)
    return ancestors

def find_common_ancestor(id1, id2, tree):
    ancestors1 = find_ancestors(id1, tree)
    ancestors2 = find_ancestors(id2, tree)
    
    common_ancestor = None
    common_ancestor_path = []
    generations = 0

    while ancestors1 and ancestors2:
        ancestor1 = ancestors1.pop()
        ancestor2 = ancestors2.pop()
        if ancestor1 == ancestor2:
            common_ancestor = ancestor1
            common_ancestor_path.append(ancestor1)
        else:
            break
        generations += 1
    
    return common_ancestor, common_ancestor_path, generations


####################################################################################################

# Design & Script
class ACGrid(Widget):
    test2 = ObjectProperty(None)
    test1 = ObjectProperty(None)
    dna = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.test1.values = tester_name
        self.ids.test2.values = tester_name
        DNA = self.dna.text

    def btn(self):
        DNA = self.dna.text
        T1 = self.test1.text
        T2 = self.test2.text

        # If any spinner is not selected, show a popup message
        if T1 == "Person 1" or T2 == "Person 2" or DNA == "mtDNA / Y DNA":
            popup_content = Label(text='Please select values from all sections.')
            popup = Popup(title='Error', content=popup_content, size_hint=(.4, .4))
            popup.open()
            return
        
        # If same person is selected
        if T1 == T2:
            popup_content = Label(text='Tester can not be the same')
            popup = Popup(title='Error', content=popup_content, size_hint=(.4, .4))
            popup.open()
            return

        # Define IDs and DNA data to compare
        id1 = ""
        id2 = ""
        DNAtree = ""
        # TestUser Directory
        tester_dir = os.path.dirname("./TestUsers/")
        file1_path = os.path.join(tester_dir, tester_library[T1])
        file2_path = os.path.join(tester_dir, tester_library[T2])

        # when mtDNA is selected
        if DNA == "mtDNA":
            DNAtree = mtDNA_data

            with open(file1_path, "r") as f1:
                for line in f1:
                    if "mtDNA:" in line:
                        id1 = line.split("mtDNA:")[1].strip()
            
            with open(file2_path, "r") as f2:
                for line in f2:
                    if "mtDNA:" in line:
                        id2 = line.split("mtDNA:")[1].strip()

        # when Y DNA is selected
        elif DNA == "Y DNA":
            DNAtree = Y_DNA_data
            
            with open(file1_path, "r") as f1:
                for line in f1:
                    if "Y:" in line:
                        id1 = line.split("Y:")[1].strip()

            with open(file2_path, "r") as f2:
                for line in f2:
                    if "Y:" in line:
                        id2 = line.split("Y:")[1].strip()


        common_ancestor, path, generations = find_common_ancestor(id1, id2, DNAtree)

        if common_ancestor:
            print("Common ancestor:", common_ancestor)
            print("Path to common ancestor:", ' -> '.join(path))
            print("Generations between the two IDs:", generations)
        else:
            print("No common ancestor found.")


        # Extract information from Excel
        id1_match_row_nums = [index for index in excel_mt_id_col.loc[excel_mt_id_col == id1].index]
        #info_ID1 = df.iloc[excel_mt_id_col.loc[excel_mt_id_col == id1].index[0]]
        print(id1_match_row_nums)
        print("Start")
        #print(info_ID1)
        print(find_ancestors(id1,DNAtree))
        print("END")



        print("\nSelected values:")
        print("User 1:", T1)
        print(id1)
        print("User 2:", T2)
        print(id2)
        print("DNA:", DNA)


        # Plotting
        #self.plot_timeline()


# Execute the App
class AnncientConnectionApp(App):
    def build(self):
        Window.clearcolor = (.245, .245, .220, 0.5)
        return ACGrid()

if __name__ == "__main__":
    AnncientConnectionApp().run()
