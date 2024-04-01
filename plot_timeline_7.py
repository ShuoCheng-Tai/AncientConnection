#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Name: plot_timeline_7.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

## Adjust the Year to fit on map
def date_adjust(Date):
    Date_ad = Date
    if Date < 0:
        if -5000 <= Date:
            Date_ad = Date / 10
        elif -10000 <= Date < -5000: 
            Date_ad = (Date + 5000) / 20 - 500
        elif Date < -10000:
            Date_ad = -800
    return Date_ad

## Set color for better understand Gender of Testers
def dot_color(info):
    gender = info.iloc[23]
    if gender == "F":
        color = "red"
    if gender == "M":
        color = "blue"
    if gender == "U":
        color = "black"
    return color

## Create the "Timeline plot"
def plot_timeline(info_p1, info_p2, info_anc):
    # Define the time range, for easy divide ticks to 12
    start_year = -750  # BCE
    end_year = 2000  # CE
    years = np.arange(start_year, end_year + 1)

    # Define the x-axis tick interval
    tick_interval = 250
    tick_positions = np.arange(start_year, end_year + 1, tick_interval)

    # Create main plot, and subplot (Ages)
    fig, (ax_main, ax_bottom) = plt.subplots(2, 1, figsize=(30, 10), gridspec_kw={'height_ratios': [8, 1]})

# Main plot on the Timeline
    ax_main.plot(years, np.zeros_like(years), color='k')

    # Set the x-axis limits and ticks for the main plot
    ax_main.set_xlim(start_year - 100, end_year + 100) # set limits for x-axis
    ax_main.set_xticks(tick_positions) # add ticks on the plot

    # Set the x-axis tick labels for the main plot
    tick_labels = []
    for year in tick_positions:
        if year < 0:
            if year == -750: # Change the labels
                tick_labels.append('< 10000 BCE')
            elif year == -500:
                tick_labels.append('5000 BCE')
            elif year == -250:
                tick_labels.append('2500 BCE')
            else:
                tick_labels.append(f'{abs(year)} BCE')
        else:
            tick_labels.append(f'{str(year)} CE')
    ax_main.set_xticklabels(tick_labels, fontsize=20) # add labels to ticks
    ax_main.xaxis.set_ticks_position('top')  # Move x-axis labels to the top

    # Set the y-axis labels for the main plot
    longitudes = [-180, -120, -60, 0, 60, 120, 180] # use longitude as y-axis
    ax_main.set_yticks(longitudes)
    ax_main.set_yticklabels(longitudes, fontsize=20)
    ax_main.set_ylabel('Longitude', fontsize=20)

    # Add vertical lines at each tick position in the main plot
    for year in tick_positions:
        ax_main.axvline(year, color='k', linestyle='-', linewidth=1.5)



# Values from Ancestor and Testers
    Date_p1 = 1950 - int(info_p1.iloc[8])
    if int(info_p1.iloc[8]) == 0:
        Date_p1 = 1950

    Date_p2 = 1950 - int(info_p2.iloc[8])
    if int(info_p2.iloc[8]) == 0:
        Date_p2 = 1950

    Date_anc = 1950 - int(info_anc.iloc[8])
    if int(info_anc.iloc[8]) == 0:
        Date_anc = 1950

    # Adjust the date to fit in the main plot, X-AXIS
    Date_anc = date_adjust(Date_anc)
    print(Date_anc)
    Date_p1 = date_adjust(Date_p1)
    Date_p2 = date_adjust(Date_p2)
    # Set the longitude as Y-AXIS
    longitude_anc = info_anc.iloc[16]
    longitude_p1 = info_p1.iloc[16]
    longitude_p2 = info_p2.iloc[16]
    # Set the color of dots
    color_anc = dot_color(info_anc)
    color_p1 = dot_color(info_p1)
    color_p2 = dot_color(info_p2)

    # Plot dots on the main plot
    dot_years = [Date_anc, Date_p1, Date_p2] # X-AXIS
    dot_values = [longitude_anc, longitude_p1, longitude_p2]  # Y-AXIS
    dot_colors = [color_anc, color_p1, color_p2] # Dots Color
    ax_main.scatter(dot_years, dot_values, color=dot_colors, s=300)  # Size (s) set to 300

    # Connect the dots with lines
    ax_main.plot([Date_anc, Date_p1], [longitude_anc, longitude_p1], color=color_p1, linestyle='--', linewidth=3)
    ax_main.plot([Date_anc, Date_p2], [longitude_anc, longitude_p2], color=color_p2, linestyle='--', linewidth=3)

    # ID name
    ID_p1 = info_p1.iloc[2]
    ID_p2 = info_p2.iloc[2]
    ID_anc = info_anc.iloc[2]

    # Add ID name on the dots, xytext=(20, 0) to the right of the dots
    ax_main.annotate(f'{ID_p1}', (Date_p1, longitude_p1), textcoords="offset points", xytext=(20, 0), ha='left', fontsize=30) 
    ax_main.annotate(f'{ID_p2}', (Date_p2, longitude_p2), textcoords="offset points", xytext=(20, 0), ha='left', fontsize=30)
    ax_main.annotate(f'{ID_anc}', (Date_anc, longitude_anc), textcoords="offset points", xytext=(20, 0), ha='left', fontsize=30)

    # Set the background color of the main plot to a light grey
    ax_main.set_facecolor('#f0f0f0')

## Create the "Bottom plot" on the Timeline
    
    # Define periods for ages and color
    periods = [
        (-750, -250, 'beige', 'Stone Age'),
        (-250, -10, 'orange', 'Metal Ages'),
        (-10, 500, 'pink', 'Imperial'),
        (500, 1500, 'purple', 'Middle Ages'),
        (1500, 2000, 'lightblue', 'Modern')
    ]

    # Add colored rectangles and text annotations for historical periods in the bottom subplot
    for period_start, period_end, color, text in periods:
        ax_bottom.axvspan(period_start, period_end, color=color, alpha=0.5)
        ax_bottom.annotate(text, xy=((period_start + period_end) / 2, 0), xycoords='data', # set text at center
                           xytext=(0, -30), textcoords='offset points',
                           fontsize=20, ha='center', va='center', color='black',
                           bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8))

    # Bottom plot on the Timeline, remove label
    ax_bottom.set_xticklabels([''] * len(tick_positions))
    ax_bottom.plot(years, np.zeros_like(years), color='k') # Plot the timeline in the bottom subplot

    # Remove y-axis ticks and labels for the bottom subplot
    ax_bottom.set_yticks([])
    ax_bottom.set_yticklabels([])

    # Set the x-axis limits and ticks for the bottom subplot, same as main plot
    ax_bottom.set_xlim(start_year - 100, end_year + 100)
    ax_bottom.set_xticks(tick_positions)


    # Save the plot as an image file
    plt.grid(True)
    canvas = FigureCanvas(fig)
    canvas.print_figure('./plot/timeline.png', bbox_inches='tight')

    plt.close(fig)
