from tkinter import Tk
from window import Window

##Initialises the Tkinter window to a full-screen, non-resizable state
root = Tk()
root.state("zoomed")
root.resizable(False, False)
tool = Window(root)
root.mainloop()