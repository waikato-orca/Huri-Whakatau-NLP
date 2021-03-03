from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from utils import *
from sentiment import *

##Window class that populates the root window and handles all the tabs and widgets
class Window:
    def __init__(self, root):
        self.root = root
        self.sentimentModel = SentimentModel()
        self.createMenu()
        self.createTabs()
        self.createFrames()
        self.createListboxes()
        self.createLabels()
        self.createGraphs()

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
        self.sentimentFrame = ttk.LabelFrame(self.sentenceTab, text = "Sentiment")
        self.twoDGraphFrame = ttk.LabelFrame(self.sentenceTab, text = "2D Graph")
        self.legendFrame = ttk.LabelFrame(self.sentenceTab, text = "Legend")
        self.twoDGraphControlFrame = ttk.LabelFrame(self.sentenceTab, text = "2D Graph Controls")

        self.sentenceFrame.grid(row = 0, column = 0, rowspan = 3, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky="nw")
        self.sentimentFrame.grid(row = 0, column = 1, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky="nw")
        self.twoDGraphFrame.grid(row = 0, column = 3, columnspan = 2, rowspan = 3, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky = "nw")
        self.legendFrame.grid(row = 3, column = 4, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky = "nw")
        self.twoDGraphControlFrame.grid(row = 3, column = 3, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky = "nw")

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
        self.discussion_listbox.bind("<<ListboxSelect>>", self.callbackSentence)

        scrollbar2 = Scrollbar(self.twoDGraphControlFrame)
        self.twoDGraphControl_listbox = Listbox(self.twoDGraphControlFrame, width = 30, height = 12, yscrollcommand = scrollbar2.set, selectmode = BROWSE, exportselection=False)
        scrollbar2.pack(side = "right", fill = 'y')
        self.twoDGraphControl_listbox.pack()
        scrollbar2.config(command = self.twoDGraphControl_listbox.yview)
        # self.twoDGraphControl_listbox.bind("<<ListboxSelect>>", self.callback2D)
        self.fillListboxes(self.twoDGraphControl_listbox)
        self.twoDGraphControl_listbox.selection_set(first=0)

    #Creates all the required labels for the window
    def createLabels(self):
        self.polarityLabel = Label(self.sentimentFrame, text = "Polarity: ", width = 30, anchor = W, justify = LEFT)
        self.subjectivityLabel = Label(self.sentimentFrame, text = "Subjectivity: ", width = 30, anchor = W, justify = LEFT)

        self.polarityLabel.pack(padx = 5, pady = 5)
        self.subjectivityLabel.pack(padx = 5, pady = 5)

    #Creates all the graphs required for the window
    def createGraphs(self):
        fig = plt.figure(figsize = (3.9,3.1))
        fig.subplots_adjust(left = 0.2)
        ax = fig.add_subplot(111)
        twoGraph = FigureCanvasTkAgg(fig, self.twoDGraphFrame)
        twoGraph.get_tk_widget().pack(fill = "y", side = "left")
        self.twoDGraph = (fig, ax, twoGraph)

    #Fill the listboxes for the graph controls
    def fillListboxes(self, listbox):
        listbox.insert(END, "Sentiment")
        listbox.insert(END, "Topic")
        listbox.insert(END, "Questions")
        listbox.insert(END, "Personal")
        listbox.insert(END, "Turns")
        listbox.insert(END, "Words")
        listbox.insert(END, "Orderliness")
        listbox.insert(END, "Objectivity")

    #Callback for the discussion listbox
    def callbackSentence(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            user = data.split(': ')[0]
            sentence = data.split(': ')[-1]
            sentimentScore = self.sentimentModel.score(sentence)
            self.polarityLabel.configure(text = "Polarity: " + str(sentimentScore.polarity))
            self.subjectivityLabel.configure(text = "Subjectivity: " + str(sentimentScore.subjectivity))
            # if len(selection) == 1:
            plot2D(self, user, sentence, event)