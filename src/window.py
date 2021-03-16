from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from utils import *
from sentiment import *
from lda import *
from cloud import *

##Window class that populates the root window and handles all the tabs and widgets
class Window:
    def __init__(self, root):
        self.topicCollection = {}
        self.root = root
        self.sentimentModel = SentimentModel()
        self.topicModel = LDAModel(self.topicCollection)
        self.cloudModel = CloudModel()
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
        self.topicFrame = ttk.LabelFrame(self.sentenceTab, text = "Topic")
        self.cloudFrame = ttk.LabelFrame(self.sentenceTab, text = "Word Cloud")
        self.threeDGraphFrame = ttk.LabelFrame(self.sentenceTab, text = "3D Graph")
        self.threeDGraphYControlFrame = ttk.LabelFrame(self.sentenceTab, text = "Y Axis Controls")
        self.threeDGraphZControlFrame = ttk.LabelFrame(self.sentenceTab, text = "Z Axis Controls")

        self.sentenceFrame.grid(row = 0, column = 0, rowspan = 2, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky="nw")
        self.sentimentFrame.grid(row = 0, column = 1, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky="nw")
        self.twoDGraphFrame.grid(row = 0, column = 3, columnspan = 2, rowspan = 3, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky = "nw")
        self.legendFrame.grid(row = 3, column = 4, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky = "nw")
        self.twoDGraphControlFrame.grid(row = 3, column = 3, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky = "nw")
        self.topicFrame.grid(row = 0, column = 2, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky="nw")
        self.cloudFrame.grid(row = 1, column = 1, rowspan = 2, columnspan = 2, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky="nw")
        self.threeDGraphFrame.grid(row = 2, column = 0, rowspan = 3, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky="nw")
        self.threeDGraphYControlFrame.grid(row = 3, column = 1, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky="nw")
        self.threeDGraphZControlFrame.grid(row = 3, column = 2, padx = 5, pady = 5, ipadx = 5, ipady = 5, sticky="nw")

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
        self.twoDGraphControl_listbox.bind("<<ListboxSelect>>", self.callback2D)
        self.fillListboxes(self.twoDGraphControl_listbox)
        self.twoDGraphControl_listbox.selection_set(first=0)

        scrollbar3 = Scrollbar(self.threeDGraphYControlFrame)
        self.threeDGraphYControl_listbox = Listbox(self.threeDGraphYControlFrame, width = 30, height = 12, yscrollcommand = scrollbar3.set, selectmode = BROWSE, exportselection=False)
        scrollbar3.pack(side = "right", fill = 'y')
        self.threeDGraphYControl_listbox.pack()
        scrollbar3.config(command = self.threeDGraphYControl_listbox.yview)
        self.threeDGraphYControl_listbox.bind("<<ListboxSelect>>", self.callback3D)
        self.fillListboxes(self.threeDGraphYControl_listbox)
        self.threeDGraphYControl_listbox.selection_set(first=0)

        scrollbar4 = Scrollbar(self.threeDGraphZControlFrame)
        self.threeDGraphZControl_listbox = Listbox(self.threeDGraphZControlFrame, width = 30, height = 12, yscrollcommand = scrollbar4.set, selectmode = BROWSE, exportselection=False)
        scrollbar4.pack(side = "right", fill = 'y')
        self.threeDGraphZControl_listbox.pack()
        scrollbar4.config(command = self.threeDGraphZControl_listbox.yview)
        self.threeDGraphZControl_listbox.bind("<<ListboxSelect>>", self.callback3D)
        self.fillListboxes(self.threeDGraphZControl_listbox)
        self.threeDGraphZControl_listbox.selection_set(first=1)

    #Creates all the required labels for the window
    def createLabels(self):
        self.polarityLabel = Label(self.sentimentFrame, text = "Polarity: ", width = 30, anchor = W, justify = LEFT)
        self.subjectivityLabel = Label(self.sentimentFrame, text = "Subjectivity: ", width = 30, anchor = W, justify = LEFT)
        self.topicLabel = Label(self.topicFrame, text = "Topic: ", width = 30, anchor = W, justify = LEFT)
        self.termsLabel = Label(self.topicFrame, text = "Terms: ", width = 30, anchor = W, justify = LEFT)

        self.polarityLabel.pack(padx = 5, pady = 5)
        self.subjectivityLabel.pack(padx = 5, pady = 5)
        self.topicLabel.pack(padx = 5, pady = 5)
        self.termsLabel.pack(padx = 5, pady = 5)

    #Creates all the graphs required for the window
    def createGraphs(self):
        fig = plt.figure(figsize = (4.3,4.2))
        fig.subplots_adjust(left = 0.2, bottom= 0.2)
        ax = fig.add_subplot(111)
        twoGraph = FigureCanvasTkAgg(fig, self.twoDGraphFrame)
        twoGraph.get_tk_widget().pack(fill = "y", side = "left")
        self.twoDGraph = (fig, ax, twoGraph)

        fig = plt.figure(figsize = (4.8,3))
        ax = fig.add_subplot(111)
        ax.axis("off")
        wordcloud = FigureCanvasTkAgg(fig, self.cloudFrame)
        wordcloud.get_tk_widget().pack(fill = "y")
        self.cloud = (fig, ax, wordcloud)

        fig = plt.figure(figsize= (3.8, 3.1))
        ax = fig.add_subplot(111, projection = '3d')
        threeGraph = FigureCanvasTkAgg(fig, self.threeDGraphFrame)
        threeGraph.get_tk_widget().pack(fill = "y", side = "left")
        ax.view_init(30, -135)
        self.threeDGraph = (fig, ax, threeGraph)

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
            topic = self.topicModel.classify(sentence)
            terms = self.topicModel.showTerms(topic)
            self.polarityLabel.configure(text = "Polarity: " + str(sentimentScore.polarity))
            self.subjectivityLabel.configure(text = "Subjectivity: " + str(sentimentScore.subjectivity))
            self.topicLabel.configure(text = "Topic: " + topic)
            self.termsLabel.configure(text = "Terms: " + terms)
            if len(selection) == 1:
                wordcloud = self.cloudModel.generate(sentence)
                self.cloud[1].imshow(wordcloud, interpolation='bilinear')
                self.cloud[0].canvas.draw()
            else:
                sentenceList = []
                for i in range(len(selection)):
                    index = selection[i]
                    data = event.widget.get(index)
                    sentence = data.split(": ")[-1]
                    sentenceList.append(sentence)
                wordcloud = self.cloudModel.batchGenerate(sentenceList)
                self.cloud[1].imshow(wordcloud, interpolation='bilinear')
                self.cloud[0].canvas.draw()
            plot2D(self, user, sentence, event, selection)
            plot3D(self, user, sentence, event, selection)

    #Callback for the change of 2-D plot metrics
    def callback2D(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            sentenceSelection = self.discussion_listbox.curselection()
            sentenceData = self.discussion_listbox.get(self.discussion_listbox.curselection()[0])
            sentence = sentenceData.split(": ")[-1]
            user = sentenceData.split(": ")[0]
            plot2D(self, user, sentence, event, sentenceSelection)

    def callback3D(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            sentenceSelection = self.discussion_listbox.curselection()
            sentenceData = self.discussion_listbox.get(self.discussion_listbox.curselection()[0])
            sentence = sentenceData.split(": ")[-1]
            user = sentenceData.split(": ")[0]
            plot3D(self, user, sentence, event, sentenceSelection)
