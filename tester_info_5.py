#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Name: tester_info_5.py

import re

## Extract infomation of Testers and Ancestor to print and plot on screen
def tester_info(info):
    master_ID = info.iloc[2]
    date = 1950 - int(info.iloc[8]) # Date
    era = "CE"
    if date < 0:
        date = -date
        era = "BCE"
    if int(info.iloc[8]) == 0:
        date = int(info.iloc[10]) # era = present
        era = ""
        if re.search(r'\(.*?\)', date):
            date = re.search(r'([\w\s-]+) \(.*?\)', date).group(1) # Get years, xxxx - xxxx

    death = info.iloc[11]
    group = info.iloc[12]
    locality = info.iloc[13]
    country = info.iloc[14]
    sex = info.iloc[23]

    return master_ID, date, era, death, locality, country, sex, group

## Use in "Description Label"
def info_translate(sex):
    if sex == 'M':
        person = "man"
        pronoun = "He"
        pronoun_low = 'he'
        sex = f"[color=#0000FF]M[/color]"
    elif sex == 'F':
        person = "woman"
        pronoun = "She"
        pronoun_low = 'she'
        sex = f"[color=#FF00FF]F[/color]"
    else:
        person = "person"
        pronoun = "The person"
        pronoun_low = 'the person'
        sex = f"[color=#800080]N/A[/color]"
    return person, pronoun, pronoun_low, sex