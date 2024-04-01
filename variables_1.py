#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Name: variables_1.py

## Read the choose DNA type tree, *used in variables(DNA_type, df)*
def read_tree(file_path):
    tree = {}
    with open(file_path, 'r') as f:
        for line in f: # Read each lines
            names = line.split()
            if len(names) == 2 and "#" not in names:
                tree[names[0]] = names[1] # Create a Library tree[child] = parent
    return tree

## Set Variables for later statement to use
def variables(DNA_type, df):
    if DNA_type == "mtDNA":

        DNA_tree = read_tree('./AncientMtDNA/mt_phyloTree_b17_Tree2.txt') # Only 1 tree will be read
        main_DNA_type = "mtDNA:"
        sec_DNA_type = "Y:"
        sec_col = 25
        DNA_sec_col = df.iloc[:,25].str.strip().astype(str)
        DNA_main_col = df.iloc[:, 28].str.strip().astype(str) # mtDNA ID column in Excel, remove spaces
        DNA_ISOGG_col = None # ISOGG column for Y DNA, no need in here
        anc_line = "maternal" # mtDNA is maternal inheritance

    elif DNA_type == "Y DNA":

        DNA_tree = read_tree('./AncientYDNA/chrY_hGrpTree_isogg2016.txt')
        main_DNA_type = "Y:"
        sec_DNA_type = "mtDNA:"
        sec_col = 28
        DNA_sec_col = df.iloc[:, 28].str.strip().astype(str)
        DNA_main_col = df.iloc[:,25].str.strip().astype(str) # Use this column to check for ID
        DNA_ISOGG_col = df.iloc[:,26].str.strip().astype(str) # This column for Tree path
        anc_line = "paternal"
        
    return DNA_tree, main_DNA_type, sec_DNA_type, DNA_sec_col, DNA_main_col, DNA_ISOGG_col, anc_line, sec_col