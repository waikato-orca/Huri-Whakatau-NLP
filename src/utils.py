from tkinter import *
from tkinter import filedialog, simpledialog
from nltk.stem import WordNetLemmatizer
from gensim.utils import simple_preprocess
from gensim.parsing import preprocessing
from sqlreader import sqlReader
from user import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import cos, pi, sin
from tkinter import messagebox
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt

#List of colors to assign to the users
COLORS = ["red", "blue", "green", "purple", "black", "orange", "pink", "brown"]

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
    window.vectorModel.train(window.sentences)
    window.topicModel.train(window.sentences)
    getTopicCollection(window)
    window.user_responses = window.vectorModel.infer(window.users, window.sentences, window.topicModel, window)
    window.discussion_listbox.delete(0, END)
    for child in window.legendFrame.winfo_children():
        child.destroy()
    for child in window.legendFrameB.winfo_children():
        child.destroy()
    populateLegend(window, window.legendFrame, "top")
    populateLegend(window, window.legendFrameB, "left")
    for child in window.polyFrameB.winfo_children():
        child.destroy()
    window.baryIndex = 0
    window.transform = simpledialog.askstring(title = "Barycentric Transformation", prompt = "Choose the barycentric transformation variant: Self(S) or Nonself(N)", parent = window.root)
    if window.transform.lower() == "s" or window.transform.lower() == "self":
        createBaryPlots(window, "self")
    elif window.transform.lower() == "n" or window.transform.lower() == "nonself":
        createBaryPlots(window, "nonself")
    showDiscussion(window)
    window.resultsFile = open("results.csv", "a+")
    window.resultsFile.write(window.dirname)
    for user in window.distinct_users:
        window.resultsFile.write("," + user.name)
    window.resultsFile.write(",user\n")

#Displays the discussion in the given format to view the raw data
def showDiscussion(window):
    for sentence, user in zip(window.sentences, window.users):
            window.discussion_listbox.insert(END, user + ": " + sentence)
            # self.discussion_listbox2.insert(END, user + ": " + sentence)

#Get the list of distinct users present in the discussion
def getDistinctUsers(window, users):
    distinct_users = []
    for user in users:
        if not checkUser(user, distinct_users):
            userObj = User(user)
            distinct_users.append(userObj)
    return distinct_users

#Creates the labels for the distinct users and populates the legend frames
def populateLegend(window, widget, side):
    for user in window.distinct_users:
        label = Label(widget, text = user.name, foreground = getColor(window.distinct_users, user.name))
        label.pack(padx = 5, pady = 5, side = side)

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
        if plotSelection == "Sentiment":
            x.append(index)
            if window.sentimentModel.model == "vader":
                if sentimentScore["compound"] != 0:
                    y.append(sentimentScore["compound"])
                elif sentimentScore["pos"] != 0:
                    y.append(sentimentScore["pos"])
                elif sentimentScore["neg"] != 0:
                    y.append(sentimentScore["neg"])
                else:
                    y.append(0.0)
            else:
                y.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
            ax.set_ylim(-2, 2)
        elif plotSelection == "Topic":
            x.append(index)
            y.append(topic)
            ax.set_ylim(-1,3)
        elif plotSelection == "Questions":
            x.append(index)
            if window.questionModel.isQuestion(sentence):
                y.append(1)
            else:
                y.append(0)
            ax.set_ylim(-0.5, 1.5)
        elif plotSelection == "Personal":
            x.append(index)
            if window.posTagger.isPersonal(sentence):
                y.append(1)
            else:
                y.append(0)
            ax.set_ylim(-0.5, 1.5)
        elif plotSelection == "Turns":
            x.append(index)
            y.append(1)
            ax.set_ylim(-0.5, 1.5)
        elif plotSelection == "Words":
            x.append(index)
            y.append(len(simple_preprocess(sentence)))
            ax.set_ylim(-0.5, 60)
        ax.scatter(x, y, label = user, color = getColor(window.distinct_users, user))
    else:
        resetCounts(window.distinct_users)
        for duser in window.distinct_users:
            x = []
            y = []
            for i in range(len(selection)):
                index = selection[i]
                data = window.discussion_listbox.get(index)
                if len(data.split(': ')) > 2:
                    sentence = ""
                    temp = data.split(': ')[1:]
                    for sent in temp:
                        sentence += sent + " "
                else:
                    sentence = data.split(': ')[-1]
                user = data.split(": ")[0]
                sentimentScore = window.sentimentModel.score(sentence)
                topic = window.topicCollection[window.topicModel.classify(sentence)]["index"]
                if user == duser.name:
                    if plotSelection == "Sentiment":
                        x.append(index)
                        if window.sentimentModel.model == "vader":
                            if sentimentScore["compound"] != 0:
                                y.append(sentimentScore["compound"])
                            elif sentimentScore["pos"] != 0:
                                y.append(sentimentScore["pos"])
                            elif sentimentScore["neg"] != 0:
                                y.append(sentimentScore["neg"])
                            else:
                                y.append(0.0)
                        else:
                            y.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
                        ax.set_ylim(-2, 2)
                    elif plotSelection == "Topic":
                        x.append(index)
                        y.append(topic)
                        ax.set_ylim(-1, 3)
                    elif plotSelection == "Questions":
                        x.append(index)
                        if window.questionModel.isQuestion(sentence):
                            duser.questionCount += 1
                        y.append(duser.questionCount)
                        print(duser.name + " " + str(duser.questionCount))
                        ax.set_ylim(-1, 15)
                    elif plotSelection == "Personal":
                        x.append(index)
                        if window.posTagger.isPersonal(sentence):
                            duser.pronounCount += 1
                        y.append(duser.pronounCount)
                        print(duser.name + " " + str(duser.pronounCount))
                        ax.set_ylim(-1, 30)
                    elif plotSelection == "Turns":
                        x.append(index)
                        duser.turnCount += 1
                        y.append(duser.turnCount)
                        print(duser.name + " " + str(duser.turnCount))
                        ax.set_ylim(-0.5, 50)
                    elif plotSelection == "Words":
                        x.append(index)
                        duser.wordCount += len(simple_preprocess(sentence))
                        y.append(duser.wordCount)
                        print(duser.name + " " + str(duser.wordCount))
                        ax.set_ylim(-0.5, 300)
            if len(x) == 1:
                ax.scatter(x, y, label = duser.name, color = getColor(window.distinct_users, duser.name))
            else:
                ax.plot(x, y, label = duser.name, color = getColor(window.distinct_users, duser.name))
    ax.set_xlabel("Responses")
    ax.set_xlim(0, len(window.sentences))
    ax.set_ylabel(plotSelection)
    fig.canvas.draw()

#Get the color the user is to be represented with
def getColor(distinct_users, user):
    colors = COLORS[:len(distinct_users)]
    for a_user, color in zip(distinct_users, colors):
        if a_user.name == user:
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
            if window.sentimentModel.model == "vader":
                if sentimentScore["compound"] != 0:
                    y.append(sentimentScore["compound"])
                elif sentimentScore["pos"] != 0:
                    y.append(sentimentScore["pos"])
                elif sentimentScore["neg"] != 0:
                    y.append(sentimentScore["neg"])
                else:
                    y.append(0.0)
            else:
                y.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
            ax.set_ylim(-2, 2)
        elif plotSelectionY == "Topic":
            y.append(topic)
            ax.set_ylim(-1,7)
        elif plotSelectionY == "Questions":
            if window.questionModel.isQuestion(sentence):
                y.append(1)
            else:
                y.append(0)
            ax.set_ylim(-0.5, 1.5)
        elif plotSelectionY == "Personal":
            if window.posTagger.isPersonal(sentence):
                y.append(1)
            else:
                y.append(0)
            ax.set_ylim(-0.5, 1.5)
        elif plotSelectionY == "Turns":
            x.append(index)
            y.append(1)
            ax.set_ylim(-0.5, 1.5)
        elif plotSelectionY == "Words":
            x.append(index)
            y.append(len(simple_preprocess(sentence)))
            ax.set_ylim(-0.5, 60)
        if plotSelectionZ == "Sentiment":
            if window.sentimentModel.model == "vader":
                if sentimentScore["compound"] != 0:
                    z.append(sentimentScore["compound"])
                elif sentimentScore["pos"] != 0:
                    z.append(sentimentScore["pos"])
                elif sentimentScore["neg"] != 0:
                    z.append(sentimentScore["neg"])
                else:
                    z.append(0.0)
            else:
                z.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
            ax.set_zlim(-2, 2)
        elif plotSelectionZ == "Topic":
            z.append(topic)
            ax.set_zlim(-1,7)
        elif plotSelectionZ == "Questions":
            if window.questionModel.isQuestion(sentence):
                z.append(1)
            else:
                z.append(0)
            ax.set_zlim(-0.5, 1.5)
        elif plotSelectionZ == "Personal":
            if window.posTagger.isPersonal(sentence):
                z.append(1)
            else:
                z.append(0)
            ax.set_zlim(-0.5, 1.5)
        elif plotSelectionZ == "Turns":
            x.append(index)
            z.append(1)
            ax.set_zlim(-0.5, 1.5)
        elif plotSelectionZ == "Words":
            x.append(index)
            z.append(len(simple_preprocess(sentence)))
            ax.set_zlim(-0.5, 60)
        z = np.array([z, z])
        ax.scatter3D(x, y, z, label = user, color = getColor(window.distinct_users, user))
    else:
        resetCounts(window.distinct_users)
        for duser in window.distinct_users:
            x = []
            y = []
            z = []
            for i in range(len(selection)):
                index = selection[i]
                data = window.discussion_listbox.get(index)
                if len(data.split(': ')) > 2:
                    sentence = ""
                    temp = data.split(': ')[1:]
                    for sent in temp:
                        sentence += sent + " "
                else:
                    sentence = data.split(': ')[-1]
                user = data.split(": ")[0]
                sentimentScore = window.sentimentModel.score(sentence)
                topic = window.topicCollection[window.topicModel.classify(sentence)]["index"]
                if user == duser.name:
                    if plotSelectionY == "Sentiment":
                        x.append(index)
                        if window.sentimentModel.model == "vader":
                            if sentimentScore["compound"] != 0:
                                y.append(sentimentScore["compound"])
                            elif sentimentScore["pos"] != 0:
                                y.append(sentimentScore["pos"])
                            elif sentimentScore["neg"] != 0:
                                y.append(sentimentScore["neg"])
                            else:
                                y.append(0.0)
                        else:
                            y.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
                        ax.set_ylim(-2, 2)
                    elif plotSelectionY == "Topic":
                        x.append(index)
                        y.append(topic)
                        ax.set_ylim(-1, 7)
                    elif plotSelectionY == "Questions":
                        x.append(index)
                        if window.questionModel.isQuestion(sentence):
                            duser.questionCount += 1
                        y.append(duser.questionCount)
                        ax.set_ylim(-1, 15)
                    elif plotSelectionY == "Personal":
                        x.append(index)
                        if window.posTagger.isPersonal(sentence):
                            duser.pronounCount += 1
                        y.append(duser.pronounCount)
                        ax.set_ylim(-1, 30)
                    elif plotSelectionY == "Turns":
                        x.append(index)
                        duser.turnCount += 1
                        y.append(duser.turnCount)
                        ax.set_ylim(-0.5, 50)
                    elif plotSelectionY == "Words":
                        x.append(index)
                        duser.wordCount += len(simple_preprocess(sentence))
                        y.append(duser.wordCount)
                        ax.set_ylim(-0.5, 300)
                    if plotSelectionZ == "Sentiment":
                        if window.sentimentModel.model == "vader":
                            if sentimentScore["compound"] != 0:
                                z.append(sentimentScore["compound"])
                            elif sentimentScore["pos"] != 0:
                                z.append(sentimentScore["pos"])
                            elif sentimentScore["neg"] != 0:
                                z.append(sentimentScore["neg"])
                            else:
                                z.append(0.0)
                        else:
                            z.append(sentimentScore.polarity + (0.5 * sentimentScore.subjectivity))
                        ax.set_zlim(-2, 2)
                    elif plotSelectionZ == "Topic":
                        z.append(topic)
                        ax.set_zlim(-1,7)
                    elif plotSelectionZ == "Questions":
                        if window.questionModel.isQuestion(sentence):
                            duser.questionCount += 1
                        z.append(duser.questionCount)
                        ax.set_zlim(-1, 15)
                    elif plotSelectionZ == "Personal":
                        if window.posTagger.isPersonal(sentence):
                            duser.pronounCount += 1
                        z.append(duser.pronounCount)
                        ax.set_zlim(-1, 30)
                    elif plotSelectionY == "Turns":
                        x.append(index)
                        duser.turnCount += 1
                        z.append(duser.turnCount)
                        ax.set_zlim(-0.5, 50)
                    elif plotSelectionZ == "Words":
                        x.append(index)
                        duser.wordCount += len(simple_preprocess(sentence))
                        z.append(duser.wordCount)
                        ax.set_zlim(-0.5, 300)
            z = np.array([z, z])
            if len(x) == 1:
                ax.scatter3D(x, y, z, label = duser.name, color = getColor(window.distinct_users, duser.name))
            else:
                ax.plot_wireframe(x, y, z, label = duser.name, color = getColor(window.distinct_users, duser.name))
    ax.set_xlabel("Responses")
    ax.set_xlim(0, len(window.sentences))
    ax.set_ylabel(plotSelectionY)
    ax.set_zlabel(plotSelectionZ)
    fig.canvas.draw()

#Resets the counts for all the users in the discussion to 0
def resetCounts(users):
    for user in users:
        user.resetCounts()

#Checks whether a User object of the given username exists in a list
def checkUser(username, users):
    for user in users:
        if username == user.name:
            return True
    return False

#Creates the user-specific barycentric allocation plots
def createBaryPlots(window, transform):
    if transform == "self":
        for user in window.distinct_users:
            plot_width = 13.5/float(len(window.distinct_users))
            fig = plt.figure(figsize = (plot_width,2.7))
            ax = fig.add_subplot(111)
            ax.axis("off")
            polyB = FigureCanvasTkAgg(fig, window.polyFrameB)
            polyB.get_tk_widget().pack(side = "left", anchor = 'nw')
            plotPolygonPts(ax, fig, user, window)
            textObj = ax.text(0, 1, user.name)
            window.polysB.append([fig, ax])
    else:
        for user in window.distinct_users:
            plot_width = 13.5/float(len(window.distinct_users))
            fig = plt.figure(figsize = (plot_width,2.7))
            ax = fig.add_subplot(111)
            ax.axis("off")
            polyB = FigureCanvasTkAgg(fig, window.polyFrameB)
            polyB.get_tk_widget().pack(side = "left", anchor = 'nw')
            plotPolygonPtsN(ax, fig, user, window)
            textObj = ax.text(0, 1, user.name)
            window.polysB.append([fig, ax])

#Creates the n polygon structure for the barycentric allocation
def plotPolygonPts(ax, fig, plotUser, window):
    x = []
    y = []
    n = len(window.distinct_users)
    r = 0.5 / sin(pi/n)
    angle = (2 * pi) / n
    for i in range(n):
        xcoord = r * cos(i * angle)
        x.append(xcoord)
        ycoord = r * sin(i * angle)
        y.append(ycoord)
        window.polyptsB.append([xcoord, ycoord])
    x.append(x[0])
    y.append(y[0])
    ax.plot(x, y, color = "black")
    i = 0
    for user in window.distinct_users:
        x1 = [x[i]]
        y1 = [y[i]]
        if plotUser is None:
            ax.scatter(x1, y1, color = getColor(window.distinct_users, user.name))
        elif plotUser is not None and plotUser != user:
            ax.scatter(x1, y1, color = getColor(window.distinct_users, user.name))
        elif plotUser is not None and plotUser == user:
            ax.scatter(x1, y1, color = getColor(window.distinct_users, user.name), alpha = 0.5)
        i += 1
    fig.canvas.draw()

#Creates the n-1 polygon structure for the barycentric allocation
def plotPolygonPtsN(ax, fig, plotUser, window):
    x = []
    y = []
    n = len(window.distinct_users) - 1
    r = 0.5 / sin(pi/n)
    angle = (2 * pi) / n
    for i in range(n):
        xcoord = r * cos(i * angle)
        x.append(xcoord)
        ycoord = r * sin(i * angle)
        y.append(ycoord)
        window.polyptsB.append([xcoord, ycoord])
    x.append(x[0])
    y.append(y[0])
    ax.plot(x, y, color = "black")
    i = 0
    for user in window.distinct_users:
        if user != plotUser:
            x1 = [x[i]]
            y1 = [y[i]]
            if plotUser is None:
                ax.scatter(x1, y1, color = getColor(window.distinct_users, user.name))
            elif plotUser is not None and plotUser != user:
                ax.scatter(x1, y1, color = getColor(window.distinct_users, user.name))
            elif plotUser is not None and plotUser == user:
                ax.scatter(x1, y1, color = getColor(window.distinct_users, user.name), alpha = 0.5)
            i += 1
    fig.canvas.draw()

#Allocates the vectors within the structure using their barycentric coordinates
def barycentric(window):
    sentence = ""
    vector = np.ndarray((3,))
    cuser = ""
    if window.baryIndex < len(window.sentences):
        for user in window.user_responses:
            user_dict = window.user_responses[user]
            if window.baryIndex in user_dict:
                for id in user_dict:
                    udict = user_dict[id]
                    if id == window.baryIndex:
                        sentence = udict["sentence"]
                        cuser = user
                        vector = udict["vector"]
                        break
        window.sentenceLabelB.configure(text = "Sentence: " + cuser + ": " + sentence)
        if window.transform.lower() == "s" or window.transform.lower() == "self":
            plotPolyB(cuser, vector, window)
        elif window.transform.lower() == "n" or window.transform.lower() == "nonself":
            plotPolyBN(cuser, vector, window)
        window.baryIndex += 1
    else:
        messagebox.showerror(title = "Error", message= "End of Discussion reached.")
        window.resultsFile.close()

#Plot the vectors within the structure constructed for self Q space barycentric allocation
def plotPolyB(user, cvector, window):
    hyperpara = []
    for ouser in window.user_responses:
        vector = None
        user_dict = window.user_responses[ouser]
        for id in user_dict:
            if int(id) <= window.baryIndex:
                udict = user_dict[id]
                vector = udict["vector"]
            else:
                break
        if vector is None:
            dist = -1
        else:               
            dist = ((cvector[0] - vector[0]) ** 2 + (cvector[1] - vector[1]) ** 2 + (cvector[2] - vector[2]) ** 2) ** 0.5
        hyperpara.append(dist)
    total = 0
    for distance in hyperpara:
        if distance != -1:
            total += distance
    for i in range(len(hyperpara)):
        if hyperpara[i] == 0:
            para = 2 * total + 1
        elif hyperpara[i] == -1:
            para = 0
        else:
            para = total / hyperpara[i]
        hyperpara[i] = para
    total = 0
    for distance in hyperpara:
        total += distance
    for i in range(len(hyperpara)):
        para = hyperpara[i] / total
        hyperpara[i] = para
    xcoord = 0
    ycoord = 0
    for para1, coord in zip(hyperpara, window.polyptsB):
        xcoord += para1 * coord[0]
        ycoord += para1 * coord[1]
    ax = None
    fig = None
    for i in range(len(window.distinct_users)):
        users = window.distinct_users[i]
        if users.name == user:
            ax = window.polysB[i][1]
            fig = window.polysB[i][0]
            break
    ax.scatter([xcoord], [ycoord], color = getColor(window.distinct_users, user), alpha = window.baryIndex/len(window.sentences))
    string = str(window.baryIndex)
    for para in hyperpara:
        string += "," + str(para)
    string += "," + user
    window.resultsFile.write(string + "\n")
    fig.canvas.draw()

#Plot the vectors within the structure constructed for self Q space barycentric allocation
# def plotPolyB(user, cvector, window):
#     cvector = np.array(cvector)
#     cvector = np.reshape(cvector, (1, -1))
#     hyperpara = []
#     for ouser in window.user_responses:
#         vector = None
#         user_dict = window.user_responses[ouser]
#         for id in user_dict:
#             if int(id) <= window.baryIndex:
#                 udict = user_dict[id]
#                 prevSent = udict["sentence"]
#                 vector = udict["vector"]
#             else:
#                 break
#         if vector is None:
#             dist = -1
#         else:
#             vector = np.array(vector)
#             vector = np.reshape(vector, (1, -1))              
#             dist = cosine_similarity(vector, cvector)[0][0]
#             dist = abs(dist)
#         hyperpara.append(dist)
#     total = 0
#     for distance in hyperpara:
#         if distance != -1:
#             total += distance
#     for i in range(len(hyperpara)):
#         if hyperpara[i] == -1:
#             para = 0
#         else:
#             para = hyperpara[i] / total
#         hyperpara[i] = para
#     xcoord = 0
#     ycoord = 0
#     for para1, coord in zip(hyperpara, window.polyptsB):
#         xcoord += para1 * coord[0]
#         ycoord += para1 * coord[1]
#     ax = None
#     fig = None
#     for i in range(len(window.distinct_users)):
#         users = window.distinct_users[i]
#         if users.name == user:
#             ax = window.polysB[i][1]
#             fig = window.polysB[i][0]
#             break
#     ax.scatter([xcoord], [ycoord], color = getColor(window.distinct_users, user))
#     string = str(window.baryIndex)
#     for para in hyperpara:
#         string += "," + str(para)
#     string += "," + user
#     window.resultsFile.write(string + "\n")
#     fig.canvas.draw()

#Plot the vectors within the structure constructed for non-self Q space barycentric allocation
def plotPolyBN(user, cvector, window):
    hyperpara = []
    for ouser in window.user_responses:
        if ouser != user:
            vector = None
            user_dict = window.user_responses[ouser]
            for id in user_dict:
                if int(id) <= window.baryIndex:
                    udict = user_dict[id]
                    vector = udict["vector"]
                else:
                    break
            if vector is None:
                dist = -1
            else:               
                dist = ((cvector[0] - vector[0]) ** 2 + (cvector[1] - vector[1]) ** 2 + (cvector[2] - vector[2]) ** 2) ** 0.5
            hyperpara.append(dist)
    total = 0
    for distance in hyperpara:
        if distance != -1:
            total += distance
    for i in range(len(hyperpara)):
        if hyperpara[i] == 0:
            para = 2 * total + 1
        elif hyperpara[i] == -1:
            para = 0
        else:
            para = total / hyperpara[i]
        hyperpara[i] = para
    total = 0
    for distance in hyperpara:
        total += distance
    if total == 0:
        for i in range(len(hyperpara)):
            para = 1 / len(hyperpara)
            hyperpara[i] = para
    else:
        for i in range(len(hyperpara)):
            para = hyperpara[i] / total
            hyperpara[i] = para
    xcoord = 0
    ycoord = 0
    for para1, coord in zip(hyperpara, window.polyptsB):
        xcoord += para1 * coord[0]
        ycoord += para1 * coord[1]
    ax = None
    fig = None
    for i in range(len(window.distinct_users)):
        users = window.distinct_users[i]
        if users.name == user:
            ax = window.polysB[i][1]
            fig = window.polysB[i][0]
            break
    ax.scatter([xcoord], [ycoord], color = getColor(window.distinct_users, user))
    string = str(window.baryIndex)
    for para in hyperpara:
        string += "," + str(para)
    string += "," + user
    window.resultsFile.write(string + "\n")
    fig.canvas.draw()

# #Plot the vectors within the structure constructed for non-self Q space barycentric allocation
# def plotPolyBN(user, cvector, window):
#     cvector = np.array(cvector)
#     cvector = np.reshape(cvector, (1, -1))
#     hyperpara = []
#     for ouser in window.user_responses:
#         if ouser != user:
#             vector = None
#             user_dict = window.user_responses[ouser]
#             for id in user_dict:
#                 if int(id) <= window.baryIndex:
#                     udict = user_dict[id]
#                     vector = udict["vector"]
#                 else:
#                     break
#             if vector is None:
#                 dist = -1
#             else:               
#                 vector = np.array(vector)
#                 vector = np.reshape(vector, (1, -1))              
#                 dist = cosine_similarity(vector, cvector)[0][0]
#                 dist = abs(dist)
#             hyperpara.append(dist)
#     total = 0
#     for distance in hyperpara:
#         if distance != -1:
#             total += distance
#     if total == 0:
#         for i in range(len(hyperpara)):
#             para = 1 / len(hyperpara)
#             hyperpara[i] = para
#     else:
#         for i in range(len(hyperpara)):
#             if hyperpara[i] == -1:
#                 para = 0
#             else:
#                 para = hyperpara[i] / total
#             hyperpara[i] = para
#     xcoord = 0
#     ycoord = 0
#     for para1, coord in zip(hyperpara, window.polyptsB):
#         xcoord += para1 * coord[0]
#         ycoord += para1 * coord[1]
#     ax = None
#     fig = None
#     for i in range(len(window.distinct_users)):
#         users = window.distinct_users[i]
#         if users.name == user:
#             ax = window.polysB[i][1]
#             fig = window.polysB[i][0]
#             break
#     ax.scatter([xcoord], [ycoord], color = getColor(window.distinct_users, user))
#     string = str(window.baryIndex)
#     for para in hyperpara:
#         string += "," + str(para)
#     string += "," + user
#     window.resultsFile.write(string + "\n")
#     fig.canvas.draw()

#Jump to the end of the discussion and observe the results at the end
def jump(window):
    while window.baryIndex < len(window.sentences):
        barycentric(window)
    messagebox.showerror(title = "Error", message= "End of Discussion reached.")
    window.resultsFile.close()