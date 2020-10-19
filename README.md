# Tetris Workshop -- AI @ UCI
This repository is for the Fall 2020 week #2 workshop of the Artificial Intelligence at UCI club<br>
Corresponding workshop video: https://youtu.be/ptUXxWumxfE<br>
Learn more about the club here: https://aiclub.ics.uci.edu/<br>
AI @ UCI Discord server: https://discord.gg/PRF9abQ<br>
<br>

# Prerequisites
We have provided a requirements.txt for you to setup your Python environment<br>
**Note: Pygame doesn't seem to like Python 3.9, so I strongly suggest using lower versions**<br><br>
Python 3.7.x Download: https://www.python.org/downloads/release/python-379/<br>

For IDE, I recommend PyCharm. It provides lots of tools that make development and tinkering easier:<br>
https://www.jetbrains.com/pycharm/
<br>

# Workspace Setup
1. Download this repository as a ZIP and extract the files
2. Open a terminal (Mac/Linux) or command prompt (Windows)
3. Change the current directory to the Tetris folder
```
cd /path/to/tetris/folder/
```
4. Create a virtual environment for this project
> For Mac and Linux, enter the following into terminal:
```
py -m venv tetrisenv

source tetrisenv/bin/activate

pip install -r requirements.txt
```
> For Windows, install virtual environment tool (if you haven't already):
```
pip3 install --user virtualenv
```
> Next, create and activate the virtual environment:
```
py -m venv tetrisenv

tetrisenv\Scripts\activate.bat

pip install -r requirements.txt
```
<br>

# Running the Code
Before you run the code, make sure to tinker with the settings on top of `TetrisParallel.py` so that the program will not overload your computer. For more information, check out the [configurations](#Configurations) section<br><br>
Once you've configured the settings, run the `TetrisParallel.py` file using:
```
py TetrisParallel.py
```
<br>

# Configurations
The settings on top of `TetrisParallel.py` allows you to configure:
1. How many games (and agents) there are at the same time. The more games there are, the faster the agents get better
2. How big each Tetris game's display is. Configuring the width will automatically adjust the height
3. How often the genes mutate. Larger mutation rate can lead to faster learning, however it might also "overshoot"

Feeling adventurous? Check out the global configuration file `TetrisSettings.py`. This file is for general settings such as colorings and Tetris tiles. Feel free to go ham in there, but stability is not guaranteed
<br>

# Troubleshooting
* If `py` is not a recognizable command, try `python` or `python3` instead
* If `pip` is not a recognizable command, try `pip3` instead
