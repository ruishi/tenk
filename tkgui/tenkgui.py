from tkinter import *
from tkinter.messagebox import showerror

def makeWidgets():
    window = Tk()
    window.title('TenK')

    form = Frame(window)
    form.pack()

    pbars = {}
    incrbtns = {}
    for (ix, skill) in :
        lab = Label(form, text=skill)
        #pbar = ...
        incr = Button(form, text="+", command=updateTime)
        lab.grid(row=ix, column=0)
        pbar.grid(row=ix, column=1)
        incr.grid(row=ix, column=2)
        pbars[skill] = pbar
        incrbtns[skill] = incr

    return window

def updateTime():
    user.add_time(skill, .5)
