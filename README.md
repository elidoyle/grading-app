# grading-app
TKinter GUI to help grade on Canvas in a more efficient manner.

# Install
## MacOSX

### grading-app
1. If not already installed, you need [Python version 3.12](https://www.python.org/downloads/release/python-3120/). Earlier versions may work, but this was created and tested with version 3.12.
2. Download this repository by clicking the green Code button and "Download ZIP".
3. Open Terminal.app (either search for it or Applications -> Utilities -> Terminal).
4. Run the following (changed accordingly, of course): `cd /path/to/downloaded/repository`
5. Run the command: `sh create_venv.sh`. This creates a Python virtual environment and installs the required packages.
6. To activate the environment, run the command: `source venv/bin/activate`. When you want to stop using the venv, run `deactivate`.

### Tcl/Tk
This GUI is created using the tkinter package, which is the standard Python interface to the Tcl/Tk GUI toolkit. You may be lucky and have everything installed already. Activate the venv created above (`source venv/bin/activate`) and start by running `python -m tkinter` from the command line. This should open a window demonstrating a simple Tk interface, letting you know that tkinter and Tcl/Tk is properly installed on your system.

The easiest way to install Tcl/Tk is through homebrew.
1. Install homebrew by running: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. Follow the instructions at the end of the install to add homebrew to you $PATH variable. 
3. Install the Tcl/Tk formula: `brew install tcl-tk`

Now try running `python -m tkinter` again.


## Windows
Code *should* still work, but not sure exactly how to install. Should be similar steps to MacOSX but uhh... I'm a Mac guy ¯\\_(ツ)_/¯

## Linux
I presume quite similar to the MacOSX instructions.

# Instructions
## Setting up the rubric
The rubric is configured through a JSON file called "config.json". You can edit this like any other text file in any text editor, although one with syntax highlighting may be useful. Points to deduct should be at the end of the comment surrounded by parentheses and with a minus sign (ex: "This is a comment that would take off 2 points (-2)").

If you wish to have a separate section for buttons to grade graphs (I like this), preface that section with which section to deduct points from (examples: "analysis graphs", "worksheet graphs", "MAG graphs"). defaultPoints for a graph section should be set to null.

The only thing in the actual master_grader.py file that you need to edit is CONFIG_PATH. Change this to the absolute path of the config file you want to use.

## Other parameters in config.json
### GUI Geometry
#### appWidth
How wide the app should be (in pixels, I think). I like having it about 1/4 of my total screen width and the full height so I don't have to scroll much.
#### appHeight
How tall the app should be (in pixels, I think). Any large number should suffice since the max it will allow is the full height of your screen.

### Click Coordinates
You need to tell the program where to click to place a comment and to select the GUI window. The best way to do this is to open a new Terminal window, make sure the venv is activated, and run the following: `python3 -c "exec(\"import pyautogui\npyautogui.displayMousePosition()\")"`. This will display the coordinates of your mouse as you move it around. Press Ctrl+C to exit.

#### placeCommentX
The x coordinate where the program should click to place a comment.
#### placeCommentY
The y coordinate where the program should click to place a comment.

#### appTitleBarX
The x coordinate of anywhere on the title bar (where it says "Grader") that isn't a button.
#### appTitleBarY
The y coordinate of anywhere on the title bar (where it says "Grader") that isn't a button.


## Running the GUI from Terminal
To open the app from Terminal, cd into the downloaded folder, activate the venv, and run: `python master_grader.py`. To run it again, hit the up arrow key to get to your previous commands.

## Creating a Dock icon for easy initialization
Terminal is better to start with so you can see any potential non-fatal errors. Once you ensure things work, this is a handy thing to have.
1. Open Automator.app and select File -> New -> Application.
2. Search the Actions for "Run Shell Script". Drag this over to the right side and drop it.
3. Shell: /bin/zsh
4. Pass input: to stdin
5. Type in the following, change accordingly: `source "/absolute/path/to/grading-app/venv/bin/activate"; python "/absolute/path/to/grading-app/master_grader.py"`
6. File -> Save
7. Drag from whereever you saved it in Finder to the Dock.
8. You may have to change some permissions in settings the first time you try to run it.

## Grading
Initialize a new instance of grading-app either via Terminal or the Dock. Select the upside-down teardrop shaped comment tool on Canvas and you're good to go. You can use the rubric buttons to automatically click and paste comments and adjust the section totals, or you can manually insert a comment and use the spinboxes' arrows to adjust the totals. The program clicks on Canvas at a fixed screen location, so you should drag the comment to the appropriate location.

When you're done, hit the "Copy" button on the grader and change to the Text tool on Canvas. Paste it onto the submission and adjust for no cover page, lateness, etc. Close the GUI window and reinitialize for the next student (I plan to add a reset button in the future).

# Known bugs
- The first comment you paste on a new student will cause the submission to zoom all the way out. Just click the "+" button on Canvas to zoom back in.

- If the GUI window isn't selected and you click an arrow on one of the points spinboxes, it will change by 0.25 as it should. However, clicking again will change by 0.5 instead of 0.25 (twice the lowest increment).

- Occasionaly pasting the comment will fail and you'll wind up with a comment that just has the letter "v". Delete the comment and change the point total back.

- Buttons are different shades depending on if the text wraps or not. 


# Additional comments
I plan to add some more bells and whistles at some point but felt this was complete enough to share with everyone before the end of the semester. I'll push it to the GitHub when I do.

Feel free to reach out to me at erd65@case.edu with any questions or assistance getting set up. I've found that using this really helps decrease the time it takes me to grade, and it definitely eases my hand cramps from constantly pressing Command+C and Command+V.