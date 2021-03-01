from tkinter import ttk, Menu
from utils import openFile

##Window class that populates the root window and handles all the tabs
class Window:
    def __init__(self, root):
        self.root = root
        self.createMenu()
        self.createTabs()

    #Create the menu bar and add the required options
    def createMenu(self):
        rootMenu = Menu(self.root)
        self.root.config(menu = rootMenu)
        fileMenu = Menu(rootMenu)
        rootMenu.add_cascade(label = "File", menu = fileMenu)
        fileMenu.add_command(label = "Open Discussion...", command = openFile)
        modelMenu = Menu(rootMenu)
        rootMenu.add_cascade(label = "Model", menu = modelMenu)
        modelMenu.add_command(label = "Switch Topic Model")

    #Create all the tabs for the NLP tool
    def createTabs(self):
        self.tabControl = ttk.Notebook(self.root)
        self.sentenceTab = ttk.Frame(self.tabControl)
        self.userTab = ttk.Frame(self.tabControl)
        self.topicTab = ttk.Frame(self.tabControl)
        # self.grammarTab = ttk.Frame(self.tabControl)
        self.baryTab = ttk.Frame(self.tabControl)
        self.influenceTab = ttk.Frame(self.tabControl)
        self.userMetricsTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.sentenceTab, text = "Statement Analysis")
        self.tabControl.add(self.userTab, text = "User Analysis")
        self.tabControl.add(self.topicTab, text = "Topic Extraction")
        # self.tabControl.add(self.grammarTab, text = "Grammatical Analysis")
        self.tabControl.add(self.baryTab, text = "Barycentric Allocation")
        self.tabControl.add(self.influenceTab, text = "Social Influence")
        self.tabControl.add(self.userMetricsTab, text = "User Metrics")
        self.tabControl.pack(expand = 1, fill = "both")