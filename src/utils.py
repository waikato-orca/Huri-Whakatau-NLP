from tkinter import *
from tkinter import filedialog
from sqlreader import sqlReader

#Opens the file with the raw data that is to be analysed
def openFile(window):
    file = filedialog.askopenfilename(initialdir="/Users/Admin/Desktop/Huri-Whakatau-NLP/data/raw", title="Select Discussion", filetypes=(("json files", "*.json"),("all files", "*.*")))
    filename = file.split('/')[-1]
    window.dirname = file.split('/')[-2]
    window.reader = sqlReader("root", "123456789", "jr_slack")
    sql = "(SELECT filename, dirname, text, user, ts FROM t_message WHERE subtype IS NULL and dirname = \"" + window.dirname + "\" and filename = \"" + filename + "\" UNION SELECT filename, dirname, topic, user, ts FROM t_message WHERE subtype = \"channel_topic\" AND dirname = \"" + window.dirname + "\" and filename = \"" + filename + "\" UNION SELECT filename, dirname, purpose, user, ts FROM t_message WHERE subtype = \"channel_purpose\" AND dirname = \"" + window.dirname + "\" and filename = \"" + filename + "\") ORDER BY ts"
    data = window.reader.read_data(sql)
    window.sentences, window.users = window.reader.sentenceExtraction(data)
    window.discussion_listbox.delete(0, END)
    showDiscussion(window)

#Displays the discussion in the given format to view the raw data
def showDiscussion(window):
    for sentence, user in zip(window.sentences, window.users):
            window.discussion_listbox.insert(END, user + ": " + sentence)
            # self.discussion_listbox2.insert(END, user + ": " + sentence)