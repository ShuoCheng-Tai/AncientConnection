#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Name: find_common_ancestor_4.py

## Build Ancestor path for 1 individual
def find_ancestors(node,tree):
    ancestors = []
    while node:
        ancestors.append(node)
        node = tree.get(node)
    return ancestors

## Find recent common ancestor from paths
def find_common_ancestor(main_ID_p1, main_ID_p2, tree):
    ancestors1 = find_ancestors(main_ID_p1, tree)
    ancestors2 = find_ancestors(main_ID_p2, tree)

    common_ancestor = None
    common_ancestor_path = []
    generations = 0

    while ancestors1 and ancestors2:
        ancestor1 = ancestors1.pop() # remove Unmatch ID (Not Common Ancestor)
        ancestor2 = ancestors2.pop() 
        if ancestor1 == ancestor2: # if shared common ancestor found
            common_ancestor = ancestor1
            common_ancestor_path.append(ancestor1)
        else:
            break
        generations += 1
    
    return common_ancestor, common_ancestor_path, generations

## Check for Date and Gender for Ancestor
def match_anc(DNA_main_col, DNA_ISOGG_col, DNA_type, ID_com_anc, df, Date_p1, Date_p2):
    
    row_nums_anc = [index for index in DNA_main_col[DNA_main_col == ID_com_anc].index]

    if DNA_type == "Y DNA":
        row_nums_anc = [index for index in DNA_ISOGG_col[DNA_ISOGG_col == ID_com_anc].index]

    info_anc = None
    match_rows = []
    backup_rows = []

    yng_anc = -100000

    # Ancestor mathcing IDs
    for i in row_nums_anc:
        check_date = 1950 - int(df.iloc[i,8])
        if int(df.iloc[i,8]) == 0: # 0 = present
            check_date = 1950 
        # Ancestor Era should be earlier than descendant

        if Date_p1 > check_date and Date_p2 > check_date:
            # sec_DNA_col = 25 means User choose mtDNA
            if DNA_type == "mtDNA":
                check_gender = df.iloc[i,23]
                if check_gender == "F":
                    match_rows.append(i)
                    continue
                elif check_gender == "U":
                    backup_rows.append(i)
                    continue

            # DNA_col_num = 28 means User choose Y DNA
            if DNA_type == "Y DNA":
                check_gender = df.iloc[i,23]
                if check_gender == "M":
                    match_rows.append(i)
                    continue
                elif check_gender == "U":
                    backup_rows.append(i)
                    continue 

    if len(match_rows) == 1:
        info_anc = df.iloc[match_rows[0], :]
    elif len(match_rows) == 0 and len(backup_rows) == 1:
        info_anc = df.iloc[backup_rows[0], :]
    elif len(match_rows) > 1:
        for k in match_rows:
            date = 1950 - int(df.iloc[k,8])
            if int(df.iloc[k,8]) == 0: # 0 = present
                date = 1950
            if date > yng_anc:
                yng_anc = date
                info_anc = df.iloc[k,:]
    return info_anc