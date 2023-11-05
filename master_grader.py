#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
from pynput.keyboard import Key, KeyCode, Listener
# import tkinter module 
from tkinter import *       
import tkinter.font
# Following will import tkinter.ttk module and 
# automatically override all the widgets 
# which are present in tkinter module. 
from tkinter.ttk import *


from pynput.keyboard import Key, Listener, Controller, KeyCode, GlobalHotKeys
import pyautogui
import time
import pyperclip
import sys
import re
import json
# from pprint import pprint
keyboard = Controller()

del globals()["Button"]
from tkinter import Button as tkButton


CONFIG_PATH = "/Users/eli/CWRU/TA/Spring 2023/grading-app/RCCIR-config.json"
POINTS_ENTRY_WIDTH = 5

with open(CONFIG_PATH) as json_data_file:
    config = json.load(json_data_file)
# print(config)

APP_WIDTH = config['appWidth']
APP_HEIGHT = config['appHeight']

sections = []
maxPoints = {}
points = {}
rubrics = {}
sectionTitles = {}
for section in config['sections']:
    sectionDict = config['sections'][section]
    if sectionDict['doInclude']:
        
        sections.append(section)
        rubrics[section] = sectionDict['rubric']

        if section == 'theory':
            sectionTitles[section] = "Intro/Theory"
        elif section == 'procedure':
            sectionTitles[section] = "Exp. Procedure"
        else:
            sectionTitles[section] = section.title()

        # since graph is a subsection of analysis or worksheet
        if 'graph' in section.lower():
            continue

        maxPoints[section] = sectionDict['defaultPoints']
        points[section] = sectionDict['defaultPoints']
        
        

MAX_POSSIBLE_POINTS = sum([maxPoints[section] for section in maxPoints])


# print(sumPoints())
# sys.exit(0)
class DoubleScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    keyword arguments are passed to the underlying Frame
    except the keyword arguments 'width' and 'height', which
    are passed to the underlying Canvas
    note that a widget layed out in this frame will have Canvas as self.master,
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        self.outer = Frame(master, **kwargs)

        # self.vsb = Scrollbar(self.outer, orient=VERTICAL)
        # self.vsb.grid(row=0, column=1, sticky='ns')
        # self.hsb = Scrollbar(self.outer, orient=HORIZONTAL)
        # self.hsb.grid(row=1, column=0, sticky='ew')
        self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.outer.rowconfigure(0, weight=1)
        self.outer.columnconfigure(0, weight=1)
        # self.canvas['yscrollcommand'] = self.vsb.set
        # self.canvas['xscrollcommand'] = self.hsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        # self.vsb['command'] = self.canvas.yview
        # self.hsb['command'] = self.canvas.xview

        self.inner = Frame(self.canvas)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion = (0,0, max(x2, width), max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")
        
    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        func = self.canvas.yview_scroll if event.state & 1 else self.canvas.yview_scroll
        # func = self.canvas.xview_scroll if event.state & 1 else self.canvas.yview_scroll  
        if event.num == 4 or event.delta > 0:
            func(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            func(1, "units" )
    
    def __str__(self):
        return str(self.outer)


def handleGraphButton(section, buttonIndex):
    parentSection = "".join(section.split("graphs")[:-1]).strip()
    clickAndTypeComment(sectionRubricButtons[section][buttonIndex].cget("text"), parentSection, sectionEntryNumbers[parentSection])

# TODO: add vars in here to config
def clickAndTypeComment(comment:str, section:str=None, pointStringVar:StringVar=None):
    oldclipboard = pyperclip.paste()
    (startingX, startingY) = pyautogui.position()
    pyautogui.click(config['placeCommentX'], config['placeCommentY'])
    pyautogui.click(config['placeCommentX'], config['placeCommentY'])
    # time.sleep(0.1)
    pyperclip.copy(comment)
    pyautogui.hotkey('command','v')
    # time.sleep(0.1)

    # pyautogui.moveTo(800,834)
    # pyautogui.drag(-500,0,button='left')

    # time.sleep(0.5)
    pyautogui.click(config['appTitleBarX'], config['appTitleBarY'])
    pyautogui.moveTo(startingX, startingY, duration=0.1)
    pyautogui.moveTo(config['placeCommentX'], config['placeCommentY'])
    pyperclip.copy(oldclipboard)

    deduct = re.findall("-[0-9]+[.]?[0-9]*", comment)[0]
    if "." not in deduct:
        deduct += ".0"
    
    points[section] += float(deduct)
    pointStringVar.set(points[section])
    # print(points)



# https://gist.github.com/novel-yet-trivial/2841b7b640bba48928200ff979204115
if __name__ == "__main__":    
    root = Tk()
    root.attributes('-topmost',True)
    root.title("Grader")
    # Open window having dimensions w x h
    w = APP_WIDTH
    h = APP_HEIGHT


    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    x = ws - w
    y = 0
    # print(root.geometry())
    root.geometry(f'{w}x{hs}+{x}+{y}')
    # use the Scrolled Frame just like any other Frame
    pointsFrame = Frame(root)
    pointsFrame.pack(side='top')
    
    sectionPointsFrames = {}
    i = 0
    for section in points:
        sectionPointsFrames[section] = Frame(pointsFrame)
        sectionPointsFrames[section].grid(row=i%3, column=i//3, sticky='ew')
        i += 1
    
    maxCol = i//3
    maxRow = i-1
    if i > 2:
        maxRow = 2

    total = StringVar()
    total.set(str(MAX_POSSIBLE_POINTS))
    def updateAndSumPoints():
        for section in points:
            num = sectionEntryNumbers[section]
            if num.get() == "" or num.get() == "0.00.00":
                num.set(str(points[section]))
            else:
                points[section] = float(num.get()) if num.get() != "" else points[section]
        tot = sum([points[section] for section in points])
        total.set(str(tot))
        

    sectionPointsLabels = {}
    sectionEntryNumbers = {}
    sectionEntrySpinboxes = {}
    for section in points:
        
        sectionPointsLabels[section] = Label(sectionPointsFrames[section], text=f"{sectionTitles[section]}:")
        sectionPointsLabels[section].pack()
        sectionEntryNumbers[section] = StringVar()
        sectionEntryNumbers[section].set(str(points[section]))
        sectionEntrySpinboxes[section] = Spinbox(sectionPointsFrames[section], width=POINTS_ENTRY_WIDTH, textvariable=sectionEntryNumbers[section], format="%.2f", from_=0, to=maxPoints[section]+10, increment=0.25)#, repeatdelay=1000, repeatinterval=250)
        sectionEntrySpinboxes[section].pack()

    for section in sectionEntryNumbers:
        sectionEntryNumbers[section].trace("w", lambda name, index, mode, entryNumber=sectionEntryNumbers[section]: updateAndSumPoints())
   
    sumLabel = Label(pointsFrame, textvar=total)
    sumLabel.grid(row=(maxRow//2)+1, column=maxCol+1, sticky='n')

    def copySum():
        for key in points:
            if int(points[key]) == points[key]:
                points[key] = int(points[key])

        s = ""
        for section in points:
            s += f"{sectionTitles[section]}: {points[section]}/{maxPoints[section]}\n"
        s += "--------------------\n"

        score = sum([points[section] for section in points])
        if int(score) == score:
            score = int(score)
        s += f"Total: {score}/{MAX_POSSIBLE_POINTS}\n"
        s += "(Graded by: ED)"

        pyperclip.copy(s)

    copySumButton = tkButton(pointsFrame, text="Copy", command=lambda: copySum())
    copySumButton.grid(row=maxRow//2, column=maxCol+1, sticky='s')



    frame = DoubleScrolledFrame(root, width=w, height=hs, borderwidth=2, relief=SUNKEN)
    frame.pack(side='top')
    # defaultFont = tkinter.font.nametofont("TkDefaultFont") 
    # defaultFont.configure(size=11) 

    BUTTON_WRAP_LENGTH = w-40

    coverpagesection = Label(frame, text="Cover page:")
    coverpagesection.pack(side = 'top', anchor='w')
    coverpagetext = ""
    for section in points:
        coverpagetext += f"{sectionTitles[section]}: /{maxPoints[section]}\n"
    coverpagetext += f"no cover page (-2) next time -5\nTotal: /{MAX_POSSIBLE_POINTS}"
    # coverpagetext = "Notebook: /10\nWorksheet: /30\nno cover page (-2) next time -5\nTotal: /40"
    coverpagebutton = tkButton(frame, text = "No cover page (copy text)", wraplength=BUTTON_WRAP_LENGTH, justify=LEFT,
                            command =lambda: pyperclip.copy(coverpagetext))
    coverpagebutton.pack(side = 'top', anchor='w')



    # Create a Button
    sectionRubricLabels = {}
    sectionRubricButtons = {}
    for section in sections:
        # no buttons for notebook grading
        if section == "notebook":
            continue

        sectionRubricLabels[section] = Label(frame, text=f"\n{sectionTitles[section]}:")
        sectionRubricLabels[section].pack(side = 'top', anchor='w')
        sectionRubricButtons[section] = [f"Button{i}" for i in range(len(rubrics[section]))]
        for i in range(len(sectionRubricButtons[section])):
            string = rubrics[section][i]
            # need to handle graphing sections differently since they don't have their own points
            if "graphs" in section.lower():
                sectionRubricButtons[section][i] = tkButton(frame, text = string, wraplength=BUTTON_WRAP_LENGTH, justify=LEFT,
                            command = lambda s=section,c=i: handleGraphButton(s,c))
            else:
                sectionRubricButtons[section][i] = tkButton(frame, text = string, wraplength=BUTTON_WRAP_LENGTH, justify=LEFT,
                                command = lambda s=section,c=i: clickAndTypeComment(sectionRubricButtons[s][c].cget("text"), s, sectionEntryNumbers[s]))

            sectionRubricButtons[section][i].pack(side = 'top', anchor='w')

    extraSpaceLabel = Label(frame, text=f"\nMade by Eli Doyle")
    extraSpaceLabel.pack(side = 'top', anchor='w')

    
    root.mainloop()