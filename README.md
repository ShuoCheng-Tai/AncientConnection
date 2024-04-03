# Project Title

BINP29_Project: AncientConnections (Y or mtDNA)

## Description

This is an application that allows User to explore maternal or paternal ancestral connections between 2 testers by identifying and comparing their haplogroups.
AncientConnection is built with Python and uses Kivy as framework for User Interface. 
Unlike conventional text-based results, this app provides graphical presentations, offering users a more intuitive understanding of their ancestral connections.

## Getting Started

### Dependencies

Developed on macOS Sonoma 14.4.1
Visual Studio Code <1.87.2> (Universal)

Python  <3.9.6>
Kivy    <2.3.0> (minimum requirement)
pandas  <2.2.1>
numpy   <1.26.4>
matplotlib  <3.8.3>

### Installing

pip install kivy pandas numpy matplotlib

### Roadmap

AncientConnection
|___AADR_54.1
|   |___AADR Annotation.xlsx
|
|___AncientMtDNA
|   |___mt_phyloTree_b17_Tree2.txt
|
|___AncientYDNA
|   |___chrY_hGrpTree_isogg2016.txt
|
|___flags
|   |___Falg_0f_AXXXX.png
|   |___Falg_0f_BXXXX.png
|   |..
|   |...
|
|___plot
|   |___female.png
|   |___make.png
|   |___unknown.png
|
|___README.md
|___main.py
|___variables_1.py
|___read_Tester_IDs_2.py
|___match_ID_3.py
|___find_common_ancestor_4.py
|___tester_info_5.py
|___connection_plot_6.py
|___plot_timeline_7.py
|___ancientconnection.kv

### Executing program

```
Open Terminal or Powershell.

# Move to the directory where the application files and folders are located.

cd AnncientConnection/


# Type in below command to execute AncientConnecion application

python main.py

```

## Help

```
User may have issue when plotting connection and timeline graph when resubmitting new testers
Bug fix will come in next version
```

## Authors

Tai, Shuo-Cheng (Leo)
[@ShuoCheng-Tai](https://github.com/ShuoCheng-Tai)

## Version History

* 0.2 (Not release yet)
    * Various bug fixes and optimizations
    * Still in developing
* 0.1
    * Initial Release
    * Working mtDNA haplogroup database (Y DNA in development)

## Acknowledgments
* [kivy] (https://www.youtube.com/@TechWithTim) 
* [png] (https://www.freepik.com)