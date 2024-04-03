#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Name: read_Tester_IDs.py

from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button

## read the Tester's mtDNA and Y DNA IDs
                    #  File  ,    Columns to check
def read_Tester_IDs(file_path, DNA_main_col, DNA_sec_col, DNA_ISOGG_col, main_DNA_type, sec_DNA_type):
    with open(file_path, "r") as f:
        for line in f: # Read DNA ID from Tester file
            if main_DNA_type in line:
                main_ID = line.split(main_DNA_type)[1].strip()
            if sec_DNA_type in line:
                sec_ID = line.split(sec_DNA_type)[1].strip()

    if main_ID is None:
        popup_content = Label(text=f'No {main_ID} in {f}.\nPLease select another DNA Type or Test User.')
        button = Button(text="Close")
        popup_content.add_widget(button)  # Add button to the popup content
        popup = Popup(title='Error', content=popup_content, size_hint=(.4, .4))
        popup.open()
        button.bind(on_press=popup.dismiss)  # Bind the button to close the popup when pressed
    
        return None, None, []

    # Get "Row Index Numbers" based on DNA type and IDs
    row_nums = [index for index in DNA_main_col.loc[DNA_main_col == main_ID].index]
    row_backup_nums = [index for index in DNA_sec_col.loc[DNA_sec_col == sec_ID].index]
    if len(row_nums) == 0:
        row_nums = row_backup_nums
    
    if main_DNA_type == "Y:":
        row_ISOGG_nums = [index for index in DNA_ISOGG_col.loc[DNA_ISOGG_col == sec_ID].index]
        if sec_ID is not None and len(row_ISOGG_nums) != 0:
            row_nums = row_ISOGG_nums

    return main_ID, sec_ID, row_nums
