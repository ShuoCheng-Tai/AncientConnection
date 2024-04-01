#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Name: match_ID.py

import re

## Find best matching ID by using the other DNA ID, else list all matching rows
def extract_info_from_excel(row_nums, df, DNA_type, sec_ID, sec_col):
    
    info = None
    match_rows = []
    backup_rows = []
    error_rows = []

    for i in row_nums: # Read each Matching ID Rows
    
        check_sec_ID = df.iloc[i, sec_col] # Sec DNA for checking
        check_gender = df.iloc[i,23] # Gender column

        if check_sec_ID == sec_ID: # Found Exact Match
            info = df.iloc[i,:]
            break

        if len(row_nums) == 1: # Only 1 Match
            info = df.iloc[i,:]
            break

    # Multiple Matches
        if DNA_type == "mtDNA":
            if check_gender == "F": # mtDNA -> Female(maternal)
                match_rows.append(i) # append Row No.
                continue

            elif check_gender == "U": # Take "U"nknown Gender as backup
                backup_rows.append(i) # append Row No.
                continue

            else: # "M"ale is WRONG
                error_rows.append(i) # append Row No.
                continue

        if DNA_type == "Y DNA":
            if check_gender == "M": # Y DNA -> Male(Paternal)
                match_rows.append(i)
                continue

            elif check_gender == "U": # Take "U"nknown Gender as backup, althrough "Y DNA" is Male
                backup_rows.append(i)
                continue

    if info is None: # If only Gender Match, use the info
        if len(match_rows) == 1:
            info = df.iloc[match_rows[0],:]

    return info, match_rows, backup_rows, error_rows


## Get information from matching rows to show on screen
def check_row(df, _rows):
    list_of_ID = []

    for i in _rows: # _rows contains "Row Index Numbers"
        
        Date = 1950 - int(df.iloc[i,8]) # Date
        ERA = "CE"
        if Date < 0:
            Date = -Date
            ERA = "BCE"
        if int(df.iloc[i,8]) == 0:
            Date = df.iloc[i,10] # Era = present
            ERA = ""
            if re.search(r'\(.*?\)', Date):
                Date = re.search(r'([\w\s-]+) \(.*?\)', Date).group(1) # Get years, xxxx - xxxx
        
                       # index, Master ID,     Gender,        Country
        list_of_ID.append([i, df.iloc[i,2], df.iloc[i,23], df.iloc[i,14], str(Date), ERA])

    return list_of_ID


# check for Date and Gender
def check_anc_row(df, _rows, sec_DNA_col, Date_p1, Date_p2):
    list_of_com_anc = []
    check_gender = df.iloc[i,23]
    for i in _rows:
        Date = 1950 - int(df.iloc[i,8]) # Date
        ERA = "CE"
        if int(df.iloc[i,8]) == 0:
            Date = 1950
            ERA = "BCE"
        if Date_p1 and Date_p2 > Date:
            if sec_DNA_col == 25:
                if check_gender == "F":
                                        # index, Master ID,     Gender,        Country
                    list_of_com_anc.append([i, df.iloc[i,2], df.iloc[i,23], df.iloc[i,14], str(Date), ERA])
            if sec_DNA_col == 28:
                if check_gender == "M":
                    list_of_com_anc.append([i, df.iloc[i,2], df.iloc[i,23], df.iloc[i,14], str(Date), ERA])
    
    return list_of_com_anc