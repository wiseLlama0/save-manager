# save-manager
A python program for adding new game / multiple character support to Steam games.
# Features
- Start a new game whenever you want without losing your progress on other characters
- Create multiple characters and switch between them
- Unlimited number of save files for each individual character you create
# Disclaimer
While I have done my best to test this extensively with my saves, I can make no guarantee that no damage will happen to your saves. I will do my best to keep this software updated with any bug fixes, but I am not responsible for data loss as a result of this tool. This is for people like me who are willing to risk incompatibility with game servers and/or accidental file loss to restore this functionality to my games.
# Installation
Requires Python 3
(Optional: Requires Git)

Before installing, I recommend backing up your save file manually just in case something goes wrong.

**Option 1. Download the python file**

Click on the green `Code` button and choose `Download ZIP`. Unzip this folder at the location you want to store the program (and your saves).

In the file explorer, click on the bar above as pictured below:

![image](https://github.com/wiseLlama0/save-manager/assets/114631736/c45a0b8e-33a7-488b-9106-7f8a56b753ed)

Type `cmd` and press enter.

Type `python SaveManager.py`

**Option 2. Install with Git**

To install with Git, click on the green "Code" button and copy the link https://github.com/wiseLlama0/save-manager.git.

Open a terminal and navigate to where you want to store the program.

Type `git clone https://github.com/wiseLlama0/save-manager.git`

Type `cd save-manager`

Type `python SaveManager.py`

# How to Use

When you start the program, follow the setup instructions carefully. When it asks you to select a save folder, select the folder with the name matching the steam game id that contains two files and a folder. It will contain `remote`, another file, and `remotecache.vdf`. 

This file is usually found at `Program Files (x86)/Steam/userdata/{your steam account id}/{game id}`. For example, the game id for Dragon's Dogma 2 is 2054970.

Another important note: Remember that any action which deploys new data to the game save folder (loading a save, changing your character, or starting a new character) will permanently delete whatever files are in there. Make sure save them using the Save Game function provided within this tool, or back them up manually yourself. I have done my best to add warnings and a last minute backup save option in all cases that one could accidentally destroy data, however I can make no guarantees that there is perfect coverage.

