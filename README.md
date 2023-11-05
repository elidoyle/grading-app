# grading-app
TKinter GUI to help with grading

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

# Instructions
To open the app from Terminal, cd into the downloaded folder, activate the venv, and run: `python master_grader.py`

The rubric is configured through a JSON file called "config.json". You can edit this like any other text file.
## Creating a Dock icon for easy initialization


# Known bugs



# Additional comments

Feel free to reach out to me at erd65@case.edu with any questions or assistance getting set up. I've found that really impacts the time it takes me to grade.