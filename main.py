#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

import kivy
kivy.require('2.3.0') # Set up minimum version requirement
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'resizable', False) #
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown

from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# My own scripts
import variables_1
import read_Tester_IDs_2
import match_ID_3
import find_common_ancestor_4
import tester_info_5
import connection_plot_6
import plot_timeline_7

####################################################################################################

# Set file path to directories
main_directory = os.getcwd()


# TestUser Directory, from Names of Testers to files
files = os.listdir("./TestUsers")
tester_file = [file for file in files if re.match(r"Test\d+.txt", file) and "DNA" not in file and file.endswith(".txt")] ## Search files that Match Test*.txt, but No "DNA" in it
sorted_files = sorted(tester_file, key=lambda x: int(re.search(r'\d+', x).group())) ## Sort the list of files numerically
# Create a Dictionary for DropDown List -> File.txts
tester_name = [os.path.splitext(file)[0] for file in sorted_files] ## Extract the names from the sorted files
tester_library = {name: file for name, file in zip(tester_name, sorted_files)} ## Assign names to files and store in a dictionary

# Extract data from Excel sheet
df = pd.read_excel('./AADR_54.1/AADR Annotation.xlsx')
# For Plot images
flags = os.listdir("./flags")

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


    def choose_ID_p1(self, select_ID, popup_instance): # Person 1 ID selected
        self.info_p1 = df.iloc[select_ID,:] # Assign the selected Value
        popup_instance.dismiss() # Close the Popup screen
        if self.info_p1 is not None and self.info_p2 is not None:
            self.continue_execution() # Continue with New funcion

    def choose_ID_p2(self, select_ID, popup_instance): # Person 2 ID selected
        self.info_p2 = df.iloc[select_ID,:]
        popup_instance.dismiss()
        if self.info_p1 is not None and self.info_p2 is not None:
            self.continue_execution()


    def continue_execution(self): # After all values are selected

        ## find_common_ancestor_4.py, Find Common Ancestor based on both ID
        ID_com_anc, path, generations = find_common_ancestor_4.find_common_ancestor(self.main_ID_p1, self.main_ID_p2, self.DNA_tree)
        ## IF no Common Ancestor, Pop Up to notift User
        if ID_com_anc is None:
            popup_content = Label(text=f'No common ancestor found.\nPlease try other Testers')
            popup = Popup(title='No Ancestor Found', content=popup_content, size_hint=(.4, .4))
            popup.open()
            return
        
        # Common Ancestor returns an ID, need to find which is the best ID to fit in (Consider both Gender and Years)

        ## Caluate years for Person 1 and 2
        Date_p1 = 1950 - int(self.info_p1.iloc[8])
        if int(self.info_p1.iloc[8]) == 0:
            Date_p1 = 1950
        Date_p2 = 1950 - int(self.info_p2.iloc[8])
        if int(self.info_p2.iloc[8]) == 0:
            Date_p2 = 1950

        ### match_anc, find multiple matching Ancestor ID, take the "Correct gender" and "Most recent year" but older than both Testers
        self.info_anc  = find_common_ancestor_4.match_anc(self.DNA_main_col, self.DNA_ISOGG_col, self.dna.text, ID_com_anc, df, Date_p1, Date_p2)

        ## IF no Mathcing Common Ancestor ID, Pop Up to notift User
        if self.info_anc is None:
            popup_content = Label(text=f'No common ancestor found.\nPlease try other Testers')
            popup = Popup(title='No Ancestor Found', content=popup_content, size_hint=(.4, .4))
            popup.open()
            return

    # Print out information
        ## tester_info_5.py, Extract infomation of Testers and Ancestor to print and plot on screen
        master_ID_p1, date_p1, era_p1, death_p1, locality_p1, country_p1, sex_p1, group_p1 = tester_info_5.tester_info(self.info_p1)
        master_ID_p2, date_p2, era_p2, death_p2, locality_p2, country_p2, sex_p2, group_p2 = tester_info_5.tester_info(self.info_p2)
        master_ID_anc, date_anc, era_anc, death_anc, locality_anc, country_anc, sex_anc, group_anc = tester_info_5.tester_info(self.info_anc)

        connection_count = 0000
        customer_count = 000

        # Information for
        person_p2, pronoun_p2, pronoun_low_p2, sex_p2 = tester_info_5.info_translate(sex_p2)
        person_anc, pronoun_anc, pronoun_low_anc, sex_anc = tester_info_5.info_translate(sex_anc) 

        ### Print on "Person 2 Label"
        self.ids.p2_label.text = f"[b][size=30]{master_ID_p2}\n[size=25][/b]{date_p2} {era_p2}\nSex: {sex_p2}"
        if ' ' in country_p2:
            country_p2 = country_p2.replace(' ', '_')
            flag_name = f"Flag_of_{country_p2}.png"
        else:
            flag_name = f"Flag_of_{country_p2}.png"

        #### Set "Person 2 Label" p2_label as a parent widget for "Flag"
        parent_widget = self.ids.p2_label.parent
        existing_flag_widget = self.ids.flag
        if existing_flag_widget:
            self.ids.flag.source=f'./flags/{flag_name}'
        else:
            flag_image = Image(source=f'./flags/{flag_name}', size_hint=(0.2, 0.2))
            parent_widget.add_widget(flag_image)
        
        ### Print on "Shared Ancestor Label"
        self.ids.ancestor_label.text = f"[size=23]Shared Ancestor\n[b]{master_ID_anc}  {sex_anc}\n{date_anc} {era_anc}\n[/b][size=20]{master_ID_p1} and {master_ID_p2} share a common {self.anc_line} ancestor who lived around this time."
        self.ids.ancestor_label.height = self.ids.ancestor_label.texture_size[1] # Adjust the height of the Label to fit the text content
        self.ids.ancestor_label.halign = 'left' # Align to "Left"

        ### Print on "Shared Connection Label"
        self.ids.share_label.text = f"[size=22]Shared Connection\n[b]1 in {connection_count}\n[/b][size=20]Only [b]{customer_count}[/b] customers are this closely related to [b]{master_ID_p2}[/b]."
        self.ids.share_label.height = self.ids.share_label.texture_size[1]
        self.ids.share_label.halign = 'left'

        ### Print on "Description Label"
        self.ids.description_label.text = f"[size=25][b]{master_ID_p2}[/b] was a {person_p2} who lived between [b]{date_p2} {era_p2}[/b] and was found in the region now known as [b]{locality_p2}[/b].\n\n{pronoun_p2} was associate with the [b]{group_p2}[/b] cultural group."
        self.ids.description_label.height = self.ids.description_label.texture_size[1]
        self.ids.description_label.halign = 'left'
        self.ids.description_label.padding = [20, 0] # move the full text to (20) right


    # Plot "Connection Graph" and "Timeline Plot"
        # Plot "Connection Graph" and Save at './plot/connection.png'
        connection_plot_6.connection_plot(self.info_anc, self.info_p1, self.info_p2)

        ## Set "Description Label" description_label as a parent widget for "Connection Graph"
        connect_parent_widget = self.ids.share_label.parent
        existing_connect_widget = self.ids.connection
        if existing_connect_widget:
            self.ids.connection.source=f'./plot/connection.png'
        else:
            connect_image = Image(source=f'./plot/connection.png', size_hint=(1, 1))
            connect_parent_widget.add_widget(connect_image)


        # Plot "Timeline Plot" and Save at './plot/timeline.png'
        plot_timeline_7.plot_timeline(self.info_p1, self.info_p2, self.info_anc)

        ## Set "Description Label" description_label as a parent widget for "Connection Graph"
        time_parent_widget = self.ids.description_label.parent
        existing_timeline_widget = self.ids.timeline
        if existing_timeline_widget:
            self.ids.timeline.source=f'./plot/timeline.png'
        else:
            timeline_image = Image(source=f'./plot/timeline.png', size_hint=(1, 1))
            time_parent_widget.add_widget(timeline_image)


################################################## Initial Process ##################################################
            
    def submitBtn(self):

    # Popup Blocks, prevent User from not selecting values
        ## If any spinner is not selected
        if self.test1.text == "Person 1" or self.test2.text == "Person 2" or self.dna.text == "mtDNA / Y DNA":
            popup_content = Label(text='Please select values from all sections.')
            popup = Popup(title='Error', content=popup_content, size_hint=(.4, .4))
            popup.open()
            return
        
        ## If same person is selected
        if self.test1.text == self.test2.text:
            popup_content = Label(text='Tester can not be the same')
            popup = Popup(title='Error', content=popup_content, size_hint=(.4, .4))
            popup.open()
            return

    # Set Path to Library
        ## Get the Path to selected Testers
        file1_path = os.path.join(os.path.dirname("./TestUsers/"), tester_library[self.test1.text])
        file2_path = os.path.join(os.path.dirname("./TestUsers/"), tester_library[self.test2.text])

    # From here is the process of 'Choosing Tester to compare' 
        ## variables_1.py, Set the initial variables from Type of DNA
        self.DNA_tree, self.main_DNA_type, self.sec_DNA_type, self.DNA_sec_col, self.DNA_main_col, self.DNA_ISOGG_col, self.anc_line, self.sec_col = variables_1.variables(self.dna.text, df)

        ## read_Tester_IDs_2.py, Read Testers' IDs from mtDNA and Y DNA in .txt file, create 'Matching rows index'
        self.main_ID_p1, self.sec_ID_p1, self.p1_row_nums = read_Tester_IDs_2.read_Tester_IDs(file1_path, self.DNA_main_col, self.DNA_sec_col, self.main_DNA_type, self.sec_DNA_type)
        self.main_ID_p2, self.sec_ID_p2, self.p2_row_nums = read_Tester_IDs_2.read_Tester_IDs(file2_path, self.DNA_main_col, self.DNA_sec_col, self.main_DNA_type, self.sec_DNA_type)
        
        ## match_ID_3.py, Read the EXCEL information to decide which Main ID is the best to use, by first checking Secondary ID
        self.info_p1, match_rows_p1, backup_rows_p1, error_rows_p1 = match_ID_3.extract_info_from_excel(self.p1_row_nums, df, self.dna.text, self.sec_ID_p1, self.sec_col)
        self.info_p2, match_rows_p2, backup_rows_p2, error_rows_p2 = match_ID_3.extract_info_from_excel(self.p2_row_nums, df, self.dna.text, self.sec_ID_p2, self.sec_col)

        ### check_row(df, _rows), Extract info of Rows, to show on Popup screen "Buttons"
        if self.info_p2 is None: # When there is No "Exact Match" or "Only 1 Match"
            if len(match_rows_p2) >= 1: # More than 1 "Correct Matches"
                list_of_ID_p2  = match_ID_3.check_row(df, match_rows_p2)
            elif len(match_rows_p2) == 0 and len(backup_rows_p2) >= 1: # No "Correct Match"
                list_of_ID_p2 = match_ID_3.check_row(df, backup_rows_p2)
            else:
                list_of_ID_p2 = match_ID_3.check_row(df, error_rows_p2)
            if len(list_of_ID_p2) == 1: # if only option in "Backup" or "Error" rows
                self.info_p2 = df.iloc[list_of_ID_p2[0],:]

            ## Create PopUp for User to choose a value
            popup_content = GridLayout(cols=1, padding=10, spacing=10)
            popup_content.add_widget(Label(text=f'No Exact matches, choose 1 out of {len(list_of_ID_p2)}.\nPerson 2: {self.test2.text}\n{self.dna.text} ID: {self.main_ID_p2}', size_hint_y=None, height=100))
            ## 4 Buttons in a Row
            num_buttons_per_row = 4 if len(list_of_ID_p2) > 4 else len(list_of_ID_p2)
            buttons_layout = GridLayout(cols=num_buttons_per_row, padding=20, spacing=15, pos_hint={'center_x': 0.5, 'center_y': 0.5})
            popup = Popup(title='Choose ID for Person 2', content=popup_content, size_hint=(.8, .85))
            for ID in list_of_ID_p2:
                btn_text = f"Master ID: {ID[1]}\nSex: {ID[2]}\nTime: {ID[4]} {ID[5]}\nNation: {ID[3]}"
                button = Button(text=btn_text, size_hint=(None, None), size=(280, 140), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=23)
                button.bind(on_press=lambda instance, select_ID_p2=ID[0], popup_instance=popup: self.choose_ID_p2(select_ID_p2, popup_instance))
                buttons_layout.add_widget(button)
            # Add the buttons layout to the popup content
            popup_content.add_widget(buttons_layout)
            popup.open()

            
            if self.info_p1 is None:
                pass # If info.p1 also doesn't have a value
            else:
                return # If Only need to choose 1 value, return the PopUp


        if self.info_p1 is None:
            if len(match_rows_p1) > 1:
                list_of_ID_p1 = match_ID_3.check_row(df, match_rows_p1)
            elif len(match_rows_p1) == 0 and len(backup_rows_p1) >= 1:
                list_of_ID_p1 = match_ID_3.check_row(df, backup_rows_p1)
            else:
                list_of_ID_p1 = match_ID_3.check_row(df, error_rows_p1)
            if len(list_of_ID_p1) == 1:
                self.info_p1 = df.iloc[list_of_ID_p1[0],:]

            popup_content = GridLayout(cols=1, padding=10, spacing=10)
            popup_content.add_widget(Label(text=f'No Exact matches, choose 1 out of {len(list_of_ID_p1)}.\nPerson 1: {self.test1.text}\n{self.dna.text} ID: {self.main_ID_p1}', size_hint_y=None, height=100))
            
            num_buttons_per_row = 4 if len(list_of_ID_p1) > 4 else len(list_of_ID_p1) 
            buttons_layout = GridLayout(cols=num_buttons_per_row, padding=20, spacing=15, pos_hint={'center_x': 0.5, 'center_y': 0.5})
            popup = Popup(title='Choose ID for Person 1', content=popup_content, size_hint=(.8, .85))
            for ID in list_of_ID_p1:
                btn_text = f"Master ID: {ID[1]}\nSex: {ID[2]}\nTime: {ID[4]} {ID[5]}\nNation: {ID[3]}"
                button = Button(text=btn_text, size_hint=(None, None), size=(280, 140), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=23)
                button.bind(on_press=lambda instance, select_ID_p1=ID[0], popup_instance=popup: self.choose_ID_p1(select_ID_p1, popup_instance))
                buttons_layout.add_widget(button)
            
            popup_content.add_widget(buttons_layout)
            popup.open()
            
            return
        # return to "choose_ID_p1" and "choose_ID_p2" above

################################################## if info_P1 and info_P2 don't need to select value ##################################################

        ## find_common_ancestor_4.py, Find Common Ancestor based on both ID
        ID_com_anc, path, generations = find_common_ancestor_4.find_common_ancestor(self.main_ID_p1, self.main_ID_p2, self.DNA_tree)
        ## IF no Common Ancestor, Pop Up to notift User
        if ID_com_anc is None:
            popup_content = Label(text=f'No common ancestor found.\nPlease try other Testers')
            popup = Popup(title='No Ancestor Found', content=popup_content, size_hint=(.4, .4))
            popup.open()
            return
        
        # Common Ancestor returns an ID, need to find which is the best ID to fit in (Consider both Gender and Years)

        ## Caluate years for Person 1 and 2
        Date_p1 = 1950 - int(self.info_p1.iloc[8]) # Column 8 gives more accurate year
        if int(self.info_p1.iloc[8]) == 0: # If year is 0, it means it's recent year, take 1950
            Date_p1 = 1950
        Date_p2 = 1950 - int(self.info_p2.iloc[8])
        if int(self.info_p2.iloc[8]) == 0:
            Date_p2 = 1950

        ### match_anc, find multiple matching Ancestor ID, take the "Correct gender" and "Most recent year" but older than both Testers
        self.info_anc  = find_common_ancestor_4.match_anc(self.DNA_main_col, self.DNA_ISOGG_col, self.dna.text, ID_com_anc, df, Date_p1, Date_p2)

        ## IF no Mathcing Common Ancestor ID, Pop Up to notift User
        if self.info_anc is None:
            popup_content = Label(text=f'No common ancestor found.\nPlease try other Testers')
            popup = Popup(title='No Ancestor Found', content = popup_content, size_hint=(.4, .4))
            popup.open()
            return

    # Print out information
        ## tester_info_5.py, Extract infomation of Testers and Ancestor to print and plot on screen
        master_ID_p1, date_p1, era_p1, death_p1, locality_p1, country_p1, sex_p1, group_p1 = tester_info_5.tester_info(self.info_p1)
        master_ID_p2, date_p2, era_p2, death_p2, locality_p2, country_p2, sex_p2, group_p2 = tester_info_5.tester_info(self.info_p2)
        master_ID_anc, date_anc, era_anc, death_anc, locality_anc, country_anc, sex_anc, group_anc = tester_info_5.tester_info(self.info_anc)

        connection_count = 0000
        customer_count = 000

        ## Information for "Description Label"
        person_p2, pronoun_p2, pronoun_low_p2, sex_p2 = tester_info_5.info_translate(sex_p2)
        person_anc, pronoun_anc, pronoun_low_anc, sex_anc = tester_info_5.info_translate(sex_anc) 

        ### Print on "Person 2 Label"
        self.ids.p2_label.text = f"[b][size=30]{master_ID_p2}\n[size=25][/b]{date_p2} {era_p2}\nSex: {sex_p2}"
        if ' ' in country_p2: # Translate country name and put on "Person 2 Label"
            country_p2 = country_p2.replace(' ', '_')
            flag_name = f"Flag_of_{country_p2}.png"
        else:
            flag_name = f"Flag_of_{country_p2}.png"

        #### Set "Person 2 Label" p2_label as a parent widget for "Flag"
        parent_widget = self.ids.p2_label.parent
        existing_flag_widget = self.ids.flag
        if existing_flag_widget: # If there is already a new one, resource 
            self.ids.flag.source=f'./flags/{flag_name}'
        else: # if NO "existing_flag_widget", put a NEW flag
            flag_image = Image(source=f'./flags/{flag_name}', size_hint=(0.2, 0.2))
            parent_widget.add_widget(flag_image)
        
        ### Print on "Shared Ancestor Label"
        self.ids.ancestor_label.text = f"[size=23]Shared Ancestor\n[b]{master_ID_anc}  {sex_anc}\n{date_anc} {era_anc}\n[/b][size=20]{master_ID_p1} and {master_ID_p2} share a common {self.anc_line} ancestor who lived around this time."
        self.ids.ancestor_label.height = self.ids.ancestor_label.texture_size[1] # Adjust the height of the Label to fit the text content
        self.ids.ancestor_label.halign = 'left' # Align to "Left"

        ### Print on "Shared Connection Label"
        self.ids.share_label.text = f"[size=22]Shared Connection\n[b]1 in {connection_count}\n[/b][size=20]Only [b]{customer_count}[/b] customers are this closely related to [b]{master_ID_p2}[/b]."
        self.ids.share_label.height = self.ids.share_label.texture_size[1]
        self.ids.share_label.halign = 'left'

        ### Print on "Description Label"
        self.ids.description_label.text = f"[size=25][b]{master_ID_p2}[/b] was a {person_p2} who lived between [b]{date_p2} {era_p2}[/b] and was found in the region now known as [b]{locality_p2}[/b].\n\n{pronoun_p2} was associate with the [b]{group_p2}[/b] cultural group."
        self.ids.description_label.height = self.ids.description_label.texture_size[1]
        self.ids.description_label.halign = 'left'
        self.ids.description_label.padding = [20, 0] # move the full text to (20) right


    # Plot "Connection Graph" and "Timeline Plot"
        # Plot "Connection Graph" and Save at './plot/connection.png'
        connection_plot_6.connection_plot(self.info_anc, self.info_p1, self.info_p2)

        ## Set "Description Label" description_label as a parent widget for "Connection Graph"
        connect_parent_widget = self.ids.share_label.parent
        existing_connect_widget = self.ids.connection
        if existing_connect_widget:
            connection_plot_6.connection_plot(self.info_anc, self.info_p1, self.info_p2)
            self.ids.connection.source=f'./plot/connection.png'
        else:
            connect_image = Image(source=f'./plot/connection.png', size_hint=(1, 1))
            connect_parent_widget.add_widget(connect_image)


        # Plot "Timeline Plot" and Save at './plot/timeline.png'
        plot_timeline_7.plot_timeline(self.info_p1, self.info_p2, self.info_anc)

        ## Set "Description Label" description_label as a parent widget for "Connection Graph"
        time_parent_widget = self.ids.description_label.parent
        existing_timeline_widget = self.ids.timeline
        if existing_timeline_widget:
            self.ids.timeline.source=f'./plot/timeline.png'
        else:
            timeline_image = Image(source=f'./plot/timeline.png', size_hint=(1, 1))
            time_parent_widget.add_widget(timeline_image)


# Execute the App
class AnncientConnectionApp(App):
    def build(self):
        Window.clearcolor = (.245, .245, .220, 0.5) # Set the App background color
        return ACGrid()
    
if __name__ == "__main__":
    AnncientConnectionApp().run()
