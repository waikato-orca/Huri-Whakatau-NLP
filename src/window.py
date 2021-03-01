from tkinter import *
from tkinter import ttk
from .utils import openFile

##Window class that populates the root window and handles all the tabs and widgets
class Window:
    def __init__(self, root):
        self.root = root
        self.createMenu()
        self.createTabs()
        self.createFrames()
        self.createListboxes()

    #Create the menu bar and add the required options
    def createMenu(self):
        rootMenu = Menu(self.root)
        self.root.config(menu = rootMenu)
        fileMenu = Menu(rootMenu)
        rootMenu.add_cascade(label = "File", menu = fileMenu)
        fileMenu.add_command(label = "Open Discussion...", command = lambda: openFile(self))
        modelMenu = Menu(rootMenu)
        rootMenu.add_cascade(label = "Model", menu = modelMenu)
        modelMenu.add_command(label = "Switch Topic Model")

    #Create all the tabs for the NLP tool
    def createTabs(self):
        tabControl = ttk.Notebook(self.root)
        self.sentenceTab = ttk.Frame(tabControl)
        self.userTab = ttk.Frame(tabControl)
        self.topicTab = ttk.Frame(tabControl)
        # self.grammarTab = ttk.Frame(tabControl)
        self.baryTab = ttk.Frame(tabControl)
        self.influenceTab = ttk.Frame(tabControl)
        self.userMetricsTab = ttk.Frame(tabControl)
        tabControl.add(self.sentenceTab, text = "Statement Analysis")
        tabControl.add(self.userTab, text = "User Analysis")
        tabControl.add(self.topicTab, text = "Topic Extraction")
        # tabControl.add(self.grammarTab, text = "Grammatical Analysis")
        tabControl.add(self.baryTab, text = "Barycentric Allocation")
        tabControl.add(self.influenceTab, text = "Social Influence")
        tabControl.add(self.userMetricsTab, text = "User Metrics")
        tabControl.pack(expand = 1, fill = "both")

    #Create all the label frames required for all the tabs
    def createFrames(self):
        self.sentenceFrame = ttk.LabelFrame(self.sentenceTab, text = "Sentence Data")

        self.sentenceFrame.grid(row = 0, column = 0, rowspan = 3, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky="nw")

    #Create all the listboxes required for all the tabs
    def createListboxes(self):
        scrollbar = Scrollbar(self.sentenceFrame)
        h_scrollbar = Scrollbar(self.sentenceFrame, orient = HORIZONTAL)
        self.discussion_listbox = Listbox(self.sentenceFrame, width = 60, height = 18, yscrollcommand = scrollbar.set, xscrollcommand = h_scrollbar.set, selectmode = EXTENDED, exportselection=False)
        scrollbar.pack(side = "right", fill = 'y')
        self.discussion_listbox.pack()
        h_scrollbar.pack(fill = 'x')
        scrollbar.config(command = self.discussion_listbox.yview)
        h_scrollbar.config(command = self.discussion_listbox.xview)
        # self.discussion_listbox.bind("<<ListboxSelect>>", callbackSentences)