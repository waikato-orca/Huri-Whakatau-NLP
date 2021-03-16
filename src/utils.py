from tkinter import *
from tkinter import filedialog
from nltk.stem import WordNetLemmatizer
from gensim.utils import simple_preprocess
from gensim.parsing import preprocessing
from sqlreader import sqlReader
import numpy as np

#List of colors to assign to the users
COLORS = ["red", "blue", "green", "purple", "black", "brown", "orange", "pink"]

#Opens the file with the raw data that is to be analysed
def openFile(window):
    file = filedialog.askopenfilenames(initialdir="/Users/Admin/Desktop/Huri-Whakatau-NLP/data/raw", title="Select Discussion", filetypes=(("json files", "*.json"),("all files", "*.*")))
    window.reader = sqlReader("root", "123456789", "jr_slack")
    if len(file) == 1:
        filename = file[0].split('/')[-1]
        window.dirname = file[0].split('/')[-2]
        sql = "(SELECT filename, dirname, text, user, ts FROM t_message WHERE subtype IS NULL and dirname = \"" + window.dirname + "\" and filename = \"" + filename + "\" UNION SELECT filename, dirname, topic, user, ts FROM t_message WHERE subtype = \"channel_topic\" AND dirname = \"" + window.dirname + "\" and filename = \"" + filename + "\" UNION SELECT filename, dirname, purpose, user, ts FROM t_message WHERE subtype = \"channel_purpose\" AND dirname = \"" + window.dirname + "\" and filename = \"" + filename + "\") ORDER BY ts"
        data = window.reader.read_data(sql)
    elif len(file) > 1:
        data = []
        for files in file:
            filename = files.split('/')[-1]
            window.dirname = files.split('/')[-2]
            sql = "(SELECT filename, dirname, text, user, ts FROM t_message WHERE subtype IS NULL and dirname = \"" + window.dirname + "\" and filename = \"" + filename + "\" UNION SELECT filename, dirname, topic, user, ts FROM t_message WHERE subtype = \"channel_topic\" AND dirname = \"" + window.dirname + "\" and filename = \"" + filename + "\" UNION SELECT filename, dirname, purpose, user, ts FROM t_message WHERE subtype = \"channel_purpose\" AND dirname = \"" + window.dirname + "\" and filename = \"" + filename + "\") ORDER BY ts"
            data.extend(window.reader.read_data(sql))
    window.sentences, window.users = window.reader.sentenceExtraction(data)
    window.distinct_users = getDistinctUsers(window, window.users)
    window.discussion_listbox.delete(0, END)
    for child in window.legendFrame.winfo_children():
        child.destroy()
    populateLegend(window, window.legendFrame)
    showDiscussion(window)
    window.topicModel.train(window.sentences)
    getTopicCollection(window)

#Displays the discussion in the given format to view the raw data
def showDiscussion(window):
    for sentence, user in zip(window.sentences, window.users):
            window.discussion_listbox.insert(END, user + ": " + sentence)
            # self.discussion_listbox2.insert(END, user + ": " + sentence)

#Get the list of distinct users present in the discussion
def getDistinctUsers(window, users):
    distinct_users = []
    for user in users:
        if user not in distinct_users:
            distinct_users.append(user)
    return distinct_users

#Creates the labels for the distinct users and populates the legend frames
def populateLegend(window, widget):
    for user in window.distinct_users:
        label = Label(widget, text = user, foreground = getColor(window.distinct_users, user))
        label.pack(padx = 5, pady = 5)

#Plots the data on the 2-D Graph based on the metric selected
def plot2D(window, user, sentence, event, selection):
    index = window.discussion_listbox.curselection()[0]
    sentimentScore = window.sentimentModel.score(sentence)
    topic = window.topicCollection[window.topicModel.classify(sentence)]["index"]
    fig = window.twoDGraph[0]
    ax = window.twoDGraph[1]
    while len(ax.collections) != 0:
        ax.collections.pop()
    if len(ax.lines) != 0:
        ax.lines = []
    plotSelection = window.twoDGraphControl_listbox.get(window.twoDGraphControl_listbox.curselection()[0])
    if len(selection) == 1:
        x = []
        y = []
        x.append(index)
        if plotSelection == "Sentiment":
            y.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
            ax.set_ylim(-2, 2)
        elif plotSelection == "Topic":
            y.append(topic)
            ax.set_ylim(-1,15)
        ax.scatter(x, y, label = user, color = getColor(window.distinct_users, user))
    else:
        for duser in window.distinct_users:
            x = []
            y = []
            for i in range(len(selection)):
                index = selection[i]
                data = window.discussion_listbox.get(index)
                sentence = data.split(": ")[-1]
                user = data.split(": ")[0]
                sentimentScore = window.sentimentModel.score(sentence)
                topic = window.topicCollection[window.topicModel.classify(sentence)]["index"]
                if user == duser:
                    if plotSelection == "Sentiment":
                        x.append(index)
                        y.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
                        ax.set_ylim(-2, 2)
                    elif plotSelection == "Topic":
                        x.append(index)
                        y.append(topic)
                        ax.set_ylim(-1, 15)
            if len(x) == 1:
                ax.scatter(x, y, label = duser, color = getColor(window.distinct_users, duser))
            else:
                ax.plot(x, y, label = duser, color = getColor(window.distinct_users, duser))
    ax.set_xlabel("Responses")
    ax.set_xlim(0, len(window.sentences))
    ax.set_ylabel(plotSelection)
    fig.canvas.draw()

#Get the color the user is to be represented with
def getColor(distinct_users, user):
    colors = COLORS[:len(distinct_users)]
    for a_user, color in zip(distinct_users, colors):
        if a_user == user:
            return color

#Creates the topic collection for easier access for other methods
def getTopicCollection(window):
    index = 0
    for topic in window.topicModel.showTopics():
        window.topicCollection[topic] = {}
        window.topicCollection[topic]["flag"] = True
        window.topicCollection[topic]["terms"] = {}
        window.topicCollection[topic]["index"] = index
        terms = window.topicModel.showTerms(topic).split(", ")
        for term in terms:
            coeff = window.topicModel.getCoeff(topic, term)
            if coeff is not None:
                window.topicCollection[topic]["terms"][term] = {}
                window.topicCollection[topic]["terms"][term]["flag"] = True
                window.topicCollection[topic]["terms"][term]["coeff"] = coeff
        index += 1

#Stems and lemmatizes the sentences
def lemmatize_stemming(text, stemmer):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

#Preprocesses the sentences to feed into other models
def preprocess(text, stemmer):
    result = []
    for token in simple_preprocess(text):
        if token not in preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token, stemmer))
    return result

#Plots the data on the 3-D plot based on the selected metrics
def plot3D(window, user, sentence, event, selection):
    index = window.discussion_listbox.curselection()[0]
    sentimentScore = window.sentimentModel.score(sentence)
    topic = window.topicCollection[window.topicModel.classify(sentence)]["index"]
    fig = window.threeDGraph[0]
    ax = window.threeDGraph[1]
    while len(ax.collections) != 0:
        ax.collections.pop()
    plotSelectionY = window.threeDGraphYControl_listbox.get(window.threeDGraphYControl_listbox.curselection()[0])
    plotSelectionZ = window.threeDGraphZControl_listbox.get(window.threeDGraphZControl_listbox.curselection()[0])
    if len(selection) == 1:
        x = []
        y = []
        z = []
        x.append(index)
        if plotSelectionY == "Sentiment":
            y.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
            ax.set_ylim(-2, 2)
        elif plotSelectionY == "Topic":
            y.append(topic)
            ax.set_ylim(-1,15)
        if plotSelectionZ == "Sentiment":
            z.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
            ax.set_zlim(-2, 2)
        elif plotSelectionZ == "Topic":
            z.append(topic)
            ax.set_zlim(-1,15)
        z = np.array([z, z])
        ax.scatter3D(x, y, z, label = user, color = getColor(window.distinct_users, user))
    else:
        for duser in window.distinct_users:
            x = []
            y = []
            z = []
            for i in range(len(selection)):
                index = selection[i]
                data = window.discussion_listbox.get(index)
                sentence = data.split(": ")[-1]
                user = data.split(": ")[0]
                sentimentScore = window.sentimentModel.score(sentence)
                topic = window.topicCollection[window.topicModel.classify(sentence)]["index"]
                if user == duser:
                    if plotSelectionY == "Sentiment":
                        x.append(index)
                        y.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
                        ax.set_ylim(-2, 2)
                    elif plotSelectionY == "Topic":
                        x.append(index)
                        y.append(topic)
                        ax.set_ylim(-1, 15)
                    if plotSelectionZ == "Sentiment":
                        z.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
                        ax.set_zlim(-2, 2)
                    elif plotSelectionZ == "Topic":
                        z.append(topic)
                        ax.set_zlim(-1,15)
            z = np.array([z, z])
            if len(x) == 1:
                ax.scatter3D(x, y, z, label = duser, color = getColor(window.distinct_users, duser))
            else:
                ax.plot_wireframe(x, y, z, label = duser, color = getColor(window.distinct_users, duser))
    ax.set_xlabel("Responses")
    ax.set_xlim(0, len(window.sentences))
    ax.set_ylabel(plotSelectionY)
    ax.set_zlabel(plotSelectionZ)
    fig.canvas.draw()