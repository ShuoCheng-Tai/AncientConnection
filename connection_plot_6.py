#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Name: connection_plot_6.py

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

## Create the "Connection Graph"
def connection_plot(anc_info, p1_info, p2_info):

    # Set image adn color to use
    # Ancestor
    anc_ID = anc_info.iloc[2]
    if anc_info.iloc[23] == "F":
        anc_gender = "./plot/female.png"
    elif anc_info.iloc[23] == "M":
        anc_gender = "./plot/male.png"
    elif anc_info.iloc[23] == "U":
        anc_gender = "./plot/unknown.png"
    anc_year = 1950 - int(anc_info.iloc[8]) # Set the Year
    anc_era = "CE"
    if anc_year < 0:
        anc_year = -anc_year
        anc_era = "BCE"
    if anc_info.iloc[8] == 0:
        anc_year = "present"
        anc_era = ""
    # Person 1
    p1_ID = p1_info.iloc[2]
    if p1_info.iloc[23] == "F":
        p1_gender = "./plot/female.png"
        line_p1 = 'red'
    elif p1_info.iloc[23] == "M":
        p1_gender = "./plot/male.png"
        line_p1 = 'blue'
    elif p1_info.iloc[23] == "U":
        p1_gender = "./plot/unknown.png"
        line_p1 = 'grey'
    p1_year = 1950 - int(p1_info.iloc[8])
    p1_era = "CE"
    if p1_year < 0:
        p1_year = -p1_year
        p1_era = "BCE"
    if p1_info.iloc[8] == 0:
        p1_year = "present"
        p1_era = ""
    # Person 2
    p2_ID = p2_info.iloc[2]
    if p2_info.iloc[23] == "F":
        p2_gender = "./plot/female.png"
        line_p2 = 'red'
    elif p2_info.iloc[23] == "M":
        p2_gender = "./plot/male.png"
        line_p2 = 'blue'
    elif p2_info.iloc[23] == "U":
        p2_gender = "./plot/unknown.png"
        line_p2 = 'grey'
    p2_year = 1950 - int(p2_info.iloc[8])
    p2_era = "CE"
    if p2_year < 0:
        p2_year = -p2_year
        p2_era = "BCE"
    if p2_info.iloc[8] == 0:
        p2_year = "present"
        p2_era = ""

    # Set the position of each node
    anc_x = 0
    anc_y = 0
    p1_x = -1
    p1_y = -1
    p2_x = 1
    p2_y = -1

    # Create the plot
    plt.figure(figsize=(5, 7))  # Set the figure size

    # Plot lines from Testers to center and then up to ancestor
    plt.plot([p1_x, p1_x, anc_x, anc_x], [p1_y, -0.2, -0.2, 0], color=line_p1, linewidth=3)  # Line from tester1 to center then to ancestor
    plt.plot([p2_x, p2_x, anc_x, anc_x], [p2_y, -0.2, -0.2, 0], color=line_p2, linewidth=3)  # Line from tester2 to center then to ancestor

    # Add images for Tester nodes
    #https://www.freepik.com/
    anc_icon = AnnotationBbox(OffsetImage(plt.imread(anc_gender), zoom=0.15), (anc_x, anc_y), frameon=False)
    p1_icon = AnnotationBbox(OffsetImage(plt.imread(p1_gender), zoom=0.15), (p1_x, p1_y), frameon=False)
    p2_icon = AnnotationBbox(OffsetImage(plt.imread(p2_gender), zoom=0.15), (p2_x, p2_y), frameon=False)

    plt.gca().add_artist(anc_icon)
    plt.gca().add_artist(p1_icon)
    plt.gca().add_artist(p2_icon)

    # Plot dots for nodes
    plt.plot(anc_x, anc_y, marker='o', markersize=10, color='grey')  # Ancestor dot
    plt.plot(p1_x, p1_y, marker='o', markersize=10, color=line_p1)  # Tester1 dot
    plt.plot(p2_x, p2_y, marker='o', markersize=10, color=line_p2)  # Tester2 dot

    # Add descriptions under the nodes
    plt.text(anc_x + 0.7, anc_y - 0.1, f"Ancestor\n{anc_ID}\n{anc_year} {anc_era}", ha='center', va='bottom', fontsize=23)
    plt.text(p1_x + 0.2, p1_y + 0.15, f"{p1_ID}\n{p1_year} {p1_era}", ha='center', va='bottom', fontsize=23) # move the text to right 0.2
    plt.text(p2_x - 0.2, p2_y + 0.15, f"{p2_ID}\n{p2_year} {p2_era}", ha='center', va='bottom', fontsize=23) # move the text to left 0.2

    plt.axis('off')  # Turn off axes

    # Save the plot as png
    plt.savefig('./plot/connection.png')

    # Close the plot
    plt.close()
