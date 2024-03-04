#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Title: ancientConnection.py
#Version: ancientConnection (1.0)
#Description: 
#Usage: 
#Input/Output: 
#Procedure: 
    

#Date­: 04/Mar/2024
#Author: Shuo-Cheng Tai (Leo)


import sys
import re
import os
import argparse

parser = argparse.ArgumentParser()

#-db DATABASE -u USERNAME
parser.add_argument("-db", "--database", help="Specify ")
parser.add_argument("-u", "--username",dest ="Username", help="User name")

args = parser.parse_args()


try:

# define the input files setting
    Script = sys.argv[0]
    InputFile = sys.argv[1]




except Exception as e:
    print(e)