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
from kivy.uix.image import Image

# Module for excel .xlsx file type
import pandas as pd

# For creating plots
import numpy as np
import matplotlib.pyplot as plt
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FigureCanvas
#from backend_kivyagg import FigureCanvasKivyAgg as FigureCanvas


#
from kivy.uix.textinput import TextInput


####################################################################################################

# Set the Directory and create Database
main_directory = os.getcwd()
files = os.listdir("./TestUsers")
flags = os.listdir("./flags")

## Test user txt files
pattern = r"Test\d+.txt" 
tester_file = [file for file in files if re.match(pattern, file) and "DNA" not in file and file.endswith(".txt")]
# Sort the list of files numerically
sorted_files = sorted(tester_file, key=lambda x: int(re.search(r'\d+', x).group()))
# Extract the names from the sorted files
tester_name = [os.path.splitext(file)[0] for file in sorted_files]

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

# mtDNA ID
excel_mt_id_col = df.iloc[:,28]
mt_id_col = excel_mt_id_col.astype(str).apply(lambda x: x.strip())


# Y DNA ID
excel_y_id_terminal_col = df.iloc[:,25]
y_id_terminal_col = excel_y_id_terminal_col.astype(str).apply(lambda x: x.strip())

## Y ID Tree ID
excel_y_id_ISOGG_col = df.iloc[:,26]
y_id_ISOGG_col = excel_y_id_ISOGG_col.astype(str).apply(lambda x: x.strip())


####################################################################################################


# Define Functions

## Find recent common ancestor from Tree
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


## Create the timeline plot
def plot_timeline():
    # Define the time range
    start_year = -10000  # BCE
    end_year = 2000  # CE
    years = np.arange(start_year, end_year + 1)

    # Define the intervals for different ages
    stone_age_end = -5000
    bronze_age_end = -1500
    iron_age_end = 500
    middle_ages_end = 1500
    modern_age_end = 2000

    # Define the colors for different ages
    colors = {
        'Stone Age': 'tan',
        'Bronze Age': 'goldenrod',
        'Iron Age': 'darkorange',
        'Middle Ages': 'saddlebrown',
        'Modern Age': 'lightgray'
    }

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the timeline with colored background for different ages
    for age, color in colors.items():
        ax.axvspan(start_year, globals()[f'{age.replace(" ", "_").lower()}_end'], color=color, alpha=0.5)

    # Plot the time line
    ax.plot(years, np.zeros_like(years), color='k')

    # Set the x-axis limits and ticks
    ax.set_xlim(start_year, end_year)
    ax.set_xticks(np.arange(start_year, end_year + 1, 250))

    # Set the x-axis labels
    ax.set_xticklabels(['Stone Age', 'Metal Ages', 'Imperial', 'Middle Ages', 'Modern'])

    # Set the x-axis label position
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_label_position('bottom')

    # Set the x-axis label rotation
    plt.xticks(rotation=45)

    # Show the plot
    plt.title('Timeline')
    plt.xlabel('Eras')
    plt.ylabel('Time')
    plt.grid(True)
    plt.show()
    return fig

####################################################################################################

# Design & Script
class ACGrid(Widget):
    test2 = ObjectProperty(None)
    test1 = ObjectProperty(None)
    dna = ObjectProperty(None)
    flag = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.test1.values = tester_name
        self.ids.test2.values = tester_name

    def btn(self):
        # Plotting
        #fig = plot_timeline()
        #canvas = FigureCanvas(fig)
        #self.ids.timeline_graph_container.add_widget(canvas)

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
        anc_line = ""
        # TestUser Directory
        tester_dir = os.path.dirname("./TestUsers/")
        file1_path = os.path.join(tester_dir, tester_library[T1])
        file2_path = os.path.join(tester_dir, tester_library[T2])

        # when mtDNA is selected
        if DNA == "mtDNA":
            DNAtree = mtDNA_data
            anc_line = "maternal"

            with open(file1_path, "r") as f1:
                for line in f1:
                    if "mtDNA:" in line:
                        id1 = line.split("mtDNA:")[1].strip()
                    if "Y:" in line:
                        id1_1 = line.split("Y:")[1].strip()
            
            with open(file2_path, "r") as f2:
                for line in f2:
                    if "mtDNA:" in line:
                        id2 = line.split("mtDNA:")[1].strip()
                    if "Y:" in line:
                        id2_1 = line.split("Y:")[1].strip()

            p1_row_nums = [index for index in mt_id_col.loc[mt_id_col == id1].index]
            p2_row_nums = [index for index in mt_id_col.loc[mt_id_col == id2].index]

        # when Y DNA is selected
        elif DNA == "Y DNA":
            DNAtree = Y_DNA_data
            anc_line = "paternal"

            with open(file1_path, "r") as f1:
                for line in f1:
                    if "Y:" in line:
                        id1 = line.split("Y:")[1].strip()
                    if "mtDNA:" in line:
                        id1_1 = line.split("mtDNA:")[1].strip()

            with open(file2_path, "r") as f2:
                for line in f2:
                    if "Y:" in line:
                        id2 = line.split("Y:")[1].strip()
                    if "mtDNA:" in line:
                        id2_1 = line.split("mtDNA:")[1].strip()

            # Y haplogroup Terminal
            p1_row_nums = [index for index in y_id_terminal_col.loc[y_id_terminal_col == id1].index]
            p2_row_nums = [index for index in y_id_terminal_col.loc[y_id_terminal_col == id2].index]

            # Check if Y DNA has match in Y haplogroup Terminal or not



        # Extract information from Excel

        ## How many matching IDs
        p1_count = 0
        p1_match_count = 0

        for i in p1_row_nums:

            if DNA == "mtDNA":

                p1_Y_ID = df.iloc[i,25]
                p1_gender = df.iloc[i,23]
                p1_count += 1

                # assume the Test is Male
                if id1_1 != "":

                    ## if mtDNA and Y DNA both math, use this individual
                    if p1_Y_ID == id1_1 and p1_gender == "M":
                        p1_info = df.iloc[i,:]
                        print("Exact matching Indicidaul: ", p1_info[2])
                        break

                    ## if no exact match, use non-female individual
                    elif p1_Y_ID != 'n/a  (sex unknown)' and p1_Y_ID != 'n/a (female)' and p1_gender == "M":
                                
                        # Extract matching row
                
                        ## if there is Y DNA ID
                        if p1_Y_ID != '..':
                            p1_info = df.iloc[i,:]
                            p1_match_count += 1
                    
                        ## if there might be a Y DNA ID
                        elif p1_Y_ID == '..':
                            ## set a backup
                            p1_backup_info = df.iloc[i,:]
                    
                    # if the person is female
                    else:
                        p1_female_info = df.iloc[i,:]


                    ## at the last index from row, check
                    if len(p1_row_nums) == p1_count:
                        # if have more than matching ones
                        if p1_match_count >= 2:
                            print("Matching P1 mtDNA:", p1_match_count)
                            print("Take last matching P1 mtDNA ID: ", p1_info[2])
                        # if no matching use backup
                        elif p1_match_count == 0 and p1_gender == "M":
                            p1_info = p1_backup_info
                            print("No matching Y DNA information.")
                        # if no backup, use Female data
                        else:
                            p1_info = p1_female_info
            

                # assume the Test is Female
                if id1_1 == "":

                    if p1_gender == "F" or p1_gender == "U":
                                
                        # Extract matching row
                
                        ## if it is Female
                        if p1_Y_ID == 'n/a (female)':
                            p1_info = df.iloc[i,:]
                            p1_match_count += 1
                    
                        ## if no Y DNA ID
                        elif p1_Y_ID == 'n/a  (sex unknown)':
                            ## set a backup
                            p1_backup_info = df.iloc[i,:]
                    # if the person is male
                    else:
                        p1_male_info = df.iloc[i,:]


                    ## at the last index from row, check
                    if len(p1_row_nums) == p1_count:
                        # if have more than matching ones
                        if p1_match_count >= 2:
                            print("Matching P1 mtDNA:", p1_match_count)
                            print("Take last matching P1 mtDNA ID: ", p1_info[2])
                        # if no matching use backup
                        elif p1_match_count == 0 and p1_gender == "F":
                            p1_info = p1_backup_info
                            print("Test Gender Unknown.")
                        # if no backup, use male data
                        else:
                            p1_info = p1_male_info

       

        ## How many matching IDs
        p2_count = 0
        p2_match_count = 0

        for i in p2_row_nums:

            if DNA == "mtDNA":

                p2_Y_ID = df.iloc[i,25]
                p2_gender = df.iloc[i,23]
                p2_count += 1

                # assume the Test is Male
                if id2_1 != "":

                    ## if mtDNA and Y DNA both math, use this individual
                    if p2_Y_ID == id2_1 and p2_gender == "M":
                        p2_info = df.iloc[i,:]
                        print("Exact matching Indicidaul: ", p2_info[2])
                        break

                    ## if no exact match, use non-female individual
                    elif p2_Y_ID != 'n/a  (sex unknown)' and p2_Y_ID != 'n/a (female)' and p2_gender == "M":

                        # Extract matching row
                
                        ## if there is Y DNA ID
                        if p2_Y_ID != '..':
                            p2_info = df.iloc[i,:]
                            p2_match_count += 1
                
                        ## if no Y DNA ID
                        elif p2_Y_ID == '..':
                            ## set a backup
                            p2_backup_info = df.iloc[i,:]
                    
                    # if the person is female
                    else:
                        p2_female_info = df.iloc[i,:]

            
                    ## at the last index from row, check
                    if len(p2_row_nums) == p2_count:
                        # if have more than matching ones
                        if p2_match_count >= 2:
                            print("Matching P2 Y DNA:", p2_match_count)
                            print("Take last matching P2 mtDNA ID: ",p2_info[2])
                        # if no matching use backup
                        elif p2_match_count == 0 and p2_gender == "M":
                            p2_info = p2_backup_info
                            print("No matching Y DNA information ")
                        # if no backup, use Female data
                        else:
                            p2_info = p2_female_info

            
                # assume the Test is Female
                if id2_1 == "":

                    if p2_gender == "F" or p2_gender == "U":
                
                        # Extract matching row
                
                        ## if it is Female
                        if p2_Y_ID == 'n/a (female)':
                            p2_info = df.iloc[i,:]
                            p2_match_count += 1
                    
                        ## if no Y DNA ID
                        elif p2_Y_ID == 'n/a  (sex unknown)':
                            ## set a backup
                            p2_backup_info = df.iloc[i,:]
                    # if the person is male
                    else:
                        p2_male_info = df.iloc[i,:]


                    ## at the last index from row, check
                    if len(p2_row_nums) == p2_count:
                        # if have more than matching ones
                        if p2_match_count >= 2:
                            print("Matching P2 mtDNA:", p2_match_count)
                            print("Take last matching P2 mtDNA ID: ", p2_info[2])
                        # if no matching use backup
                        elif p2_match_count == 0 and p2_gender == "F":
                            p2_info = p2_backup_info
                            print("Test Gender Unknown.")
                        # if no backup, use male data
                        else:
                            p2_info = p2_male_info
        





        common_ancestor, path, generations = find_common_ancestor(id1, id2, DNAtree)

        #if common_ancestor:
        #    print("Common ancestor:", common_ancestor)
        #    print("Path to common ancestor:", ' -> '.join(path))
        #    print("Generations between the two IDs:", generations)
        #else:
        #    print("No common ancestor found.")


        anc_count = 0
        anc_sex_match_count = 0
        # Ancestor mathcing IDs
        if DNA == "mtDNA":
            anc_row_nums = [index for index in mt_id_col.loc[mt_id_col == common_ancestor].index]

            for i in anc_row_nums:
                
                anc_s = df.iloc[i,23]
                anc_count += 1

                if anc_s == "F":
                    anc_info = df.iloc[i,:]
                    anc_sex_match_count += 1
                
                elif anc_s == "U":
                    anc_backup_info = df.iloc[i,:]

                elif anc_s == "M":
                    anc_Error_info = df.iloc[i,:]

                if len(anc_row_nums) == anc_count:
                    if anc_sex_match_count == 0 and anc_backup_info == True:
                        anc_info = anc_backup_info
                    elif anc_sex_match_count == 0 and anc_backup_info == False:
                        anc_info = anc_Error_info
                        print("No match Maternal line of ancestor.")

        elif DNA == "Y DNA":
            anc_row_nums = [index for index in y_id_ISOGG_col.loc[y_id_ISOGG_col == common_ancestor].index]

            for i in anc_row_nums:
                
                anc_s = df.iloc[i,23]
                anc_count += 1

                if anc_s == "M":
                    anc_info = df.iloc[i,:]
                    anc_sex_match_count += 1
                
                elif anc_s == "U":
                    anc_backup_info = df.iloc[i,:]

                elif anc_s == "F":
                    anc_Error_info = df.iloc[i,:]

                if len(anc_row_nums) == anc_count:
                    if anc_sex_match_count == 0 and anc_backup_info == True:
                        anc_info = anc_backup_info
                    elif anc_sex_match_count == 0 and anc_backup_info == False:
                        anc_info = anc_Error_info
                        print("No match Paternal line of ancestor.")

        

        p1_ID = p1_info[2]
        p1_sex = p1_info.iloc[23]
        p1_year = p1_info.iloc[10]
        p2_ID = p2_info[2]
        p2_sex = p2_info.iloc[23]
        p2_year = p2_info.iloc[10]
        p2_loc = p2_info.iloc[13]
        p2_pol_entity = p2_info.iloc[14]

        anc_ID = anc_info.iloc[2]
        anc_sex = anc_info.iloc[23]
        anc_year = anc_info.iloc[10]
        anc_death = anc_info.iloc[11]
        anc_loc = anc_info.iloc[13]
        anc_pol_entity = anc_info.iloc[14]

        
        if p2_sex == 'M':
            p2_person = "man"
            p2_pronoun = "He"
            p2_pronoun_low = 'he'
            p2_sex = f"[color=#0000FF]M[/color]"
        elif p2_sex == 'F':
            p2_person = "woman"
            p2_pronoun = "She"
            p2_pronoun_low = 'she'
            p2_sex = f"[color=#FF00FF]F[/color]"
        else:
            p2_person = "person"
            p2_pronoun = "The person"
            p2_pronoun_low = 'the person'
            p2_sex = f"[color=#800080]N/A[/color]"



        # Update the text of the Label widget with the id 'time_label'
        if re.search(r'\(.*?\)', p2_year):
            p2_year = re.search(r'([\w\s-]+) \(.*?\)', p2_year).group(1)
        
        self.ids.p2_label.text = f"[b][size=30]{p2_ID}\n[size=25][/b]{p2_year}\nSex: {p2_sex}"


    # Create an Image widget
        if ' ' in p2_pol_entity:
            p2_pol_entity = p2_pol_entity.replace(' ', '_')
            flag_name = f"Flag_of_{p2_pol_entity}.png"
        else:
            flag_name = f"Flag_of_{p2_pol_entity}.png"


        # Get the parent widget (GridLayout) of p2_label
        parent_widget = self.ids.p2_label.parent


        # Remove the existing flag widget from its current parent, if any
        existing_flag_widget = self.ids.flag


        if existing_flag_widget:
            self.ids.flag.source=f'./flags/{flag_name}'
        else:
            # Create an Image widget
            flag_image = Image(source=f'./flags/{flag_name}', size_hint=(0.2, 0.2))

            # Add the flag_image widget to the parent widget
            parent_widget.add_widget(flag_image)
        
        
        if anc_sex == 'M':
            anc_sex = f"[color=#0000FF]M[/color]"
        elif anc_sex == 'F':
            anc_sex = f"[color=#FF00FF]F[/color]"
        else:
            anc_sex = f"[color=#800080]N/A[/color]"



        # Update the text of the Label widget with the id 'time_label'
        if re.search(r'\(.*?\)', anc_year):
            anc_year = re.search(r'([\w\s-]+) \(.*?\)', anc_year).group(1)

        self.ids.ancestor_label.text = f"[size=23][/b]Shared Ancestor\n[b]{anc_ID}  {anc_sex}\n[size=23]{anc_year}\n[size=20][/b]{p1_ID} and {p2_ID} share a common {anc_line} ancestor who lived around this time."
        # Adjust the height of the Label to fit the text content
        self.ids.ancestor_label.height = self.ids.ancestor_label.texture_size[1]
        self.ids.ancestor_label.halign = 'left'

        # Update the text of the Label widget with the id 'share_label'
        self.ids.share_label.text = f"[size=22][/b]Shared Connection\n[size=22][b]1 in 1900\n[size=20][/b]Only [b]160 [/b]customers are this closely related to [b]{p2_ID}."
        # Adjust the height of the Label to fit the text content
        self.ids.share_label.height = self.ids.ancestor_label.texture_size[1]
        self.ids.share_label.halign = 'left'


        # set age of time
        #if anc_year


        # Update the text of the Label widget with the id 'description_label'
        self.ids.description_label.text = f"[size=25][b]{p2_ID}[/b] was a {p2_person} who lived between [b]{p2_year}[/b] and was found in the region now known as [b]{p2_loc}.\n\n[/b]{p2_pronoun} was associate with the"
        # Adjust the height of the Label to fit the text content
        self.ids.description_label.height = self.ids.ancestor_label.texture_size[1]
        self.ids.description_label.halign = 'left'
        self.ids.description_label.padding = [20, 0]


    # Create an Connection widget
        #if ' ' in p2_pol_entity:
        #    p2_pol_entity = p2_pol_entity.replace(' ', '_')
        #    flag_name = f"Flag_of_{p2_pol_entity}.png"
        #else:
        #    flag_name = f"Flag_of_{p2_pol_entity}.png"


        # Get the parent widget (GridLayout) of p2_label
        connect_parent_widget = self.ids.description_label.parent


        # Remove the existing flag widget from its current parent, if any
        existing_connect_widget = self.ids.connection


        if existing_connect_widget:
            self.ids.connection.source=f'./plot/connection.png'
        else:
            # Create an Image widget
            connect_image = Image(source=f'./plot/connection.png', size_hint=(1, 1))

            # Add the flag_image widget to the parent widget
            connect_parent_widget.add_widget(connect_image)



    # Create an Timeline widget
        #if ' ' in p2_pol_entity:
        #    p2_pol_entity = p2_pol_entity.replace(' ', '_')
        #    flag_name = f"Flag_of_{p2_pol_entity}.png"
        #else:
        #    flag_name = f"Flag_of_{p2_pol_entity}.png"


        # Get the parent widget (GridLayout) of p2_label
        time_parent_widget = self.ids.time_label.parent


        # Remove the existing flag widget from its current parent, if any
        existing_timeline_widget = self.ids.timeline


        if existing_timeline_widget:
            self.ids.timeline.source=f'./plot/timeline.png'
        else:
            # Create an Image widget
            timeline_image = Image(source=f'./plot/timeline.png', size_hint=(1, 1))

            # Add the flag_image widget to the parent widget
            time_parent_widget.add_widget(timeline_image)




# Execute the App
class AnncientConnectionApp(App):
    def build(self):
        Window.clearcolor = (.245, .245, .220, 0.5)
        return ACGrid()

if __name__ == "__main__":
    AnncientConnectionApp().run()
