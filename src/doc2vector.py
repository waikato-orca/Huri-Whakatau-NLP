from sklearn.datasets import fetch_20newsgroups
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from utils import *
from tkinter import messagebox
from nltk.corpus import stopwords
import numpy as np

##Doc2Vec model that will be used for inferring vectors
class VectorModel:
    def __init__(self):
        print("Vector Model: doc2vec")

    #Train the model on the discussion data provided
    def train(self, sentences):
        self.corpus = []
        newsgroups_train = fetch_20newsgroups(remove=('headers', 'footers')).data
        for text in sentences:
            self.corpus.append(text)
        stoplist = set(stopwords.words('english'))
        texts = [[word for word in document.lower().split()] for document in self.corpus]
        texts = [TaggedDocument(doc, [i]) for i, doc in enumerate(texts)]
        self.model = Doc2Vec(texts, vector_size = 3, window = 2, min_count = 1, workers = 4, epochs = 100)

    #Infer a vector for the provided sentence
    def infer(self, users, sentences, topicModel, window):
        self.user_responses = {}
        for user in users:
            if user not in self.user_responses:
                self.user_responses[user] = {}
        for i in range(len(sentences)):
            sentence = sentences[i]
            user = users[i]
            self.user_responses[user][i] = {}
            self.user_responses[user][i]["sentence"] = sentence
            self.user_responses[user][i]["vector"] = self.model.infer_vector(sentence.split())
            self.user_responses[user][i]["topic"] = topicModel.classify(sentence)
        return self.user_responses