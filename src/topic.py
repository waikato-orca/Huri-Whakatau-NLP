from nltk.stem import PorterStemmer
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from utils import *
from utils import preprocess
from nltk.stem import PorterStemmer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

##LDA model that will be used for topic extraction
class TopicModel:
    def __init__(self, topicCollection, string):
        if string.lower() == "nmf":
            self.model = "NMF"
            print("Topic Extraction Model: sklearn.NMF")
        else:
            self.model = "LDA"
            print("Topic Extraction Model: gensim.LDAModel")
        self.stemmer = PorterStemmer()

    #Train the LDA model on the current discussion
    def train(self, sentences):
        if self.model == "NMF":
            self.sentenceData = []
            for sentence in sentences:
                self.sentenceData.append(preprocess(sentence, self.stemmer))
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1500,
                ngram_range=(1, 2),
                preprocessor=' '.join,
                stop_words='english'
            )
            tfidf = self.tfidf_vectorizer.fit_transform(self.sentenceData)
            self.nmf = NMF(n_components=2, solver="mu")
            self.W = self.nmf.fit_transform(tfidf)
            self.H = self.nmf.components_
        else:
            sentenceData = []
            for sentence in sentences:
                sentenceData.append(preprocess(sentence, self.stemmer))
            self.dictionary = Dictionary(sentenceData)
            bow_corpus = [self.dictionary.doc2bow(doc) for doc in sentenceData]
            self.lda_model = LdaModel(bow_corpus, num_topics=2, id2word=self.dictionary, passes=10)

    #Classify a given sentence to one of the topics found in training
    def classify(self, sentence):
        if self.model == "NMF":
            index = self.sentenceData.index(preprocess(sentence, self.stemmer))
            topic = self.W.argmax(axis=1)[index]
            return "Topic " + str(topic)
        else:
            bow_vector = self.dictionary.doc2bow(preprocess(sentence, self.stemmer))
            return "Topic " + str(sorted(self.lda_model[bow_vector], key=lambda tup: -1*tup[1])[0][0])

    #Shows the terms of a given topic
    def showTerms(self, topic):
        if self.model == "NMF":
            terms = ""
            top_features = []
            tfidf_feature_names = self.tfidf_vectorizer.get_feature_names()
            for topic_idx, topicID in enumerate(self.H):
                if topic_idx == int(topic.split(' ')[-1]):
                    top_features_ind = topicID.argsort()[:-20 - 1:-1]
                    top_features = [tfidf_feature_names[i] for i in top_features_ind]
                    weights = topicID[top_features_ind]
            for term in top_features:
                terms += term + ", "
            print(topic.split(' ')[-1] + " " + terms)
            return terms
        else:
            terms = ""
            topic = int(topic.split(" ")[-1])
            for term in self.lda_model.show_topic(topic):
                terms += term[0] + ", "
            print(str(topic) + " " + terms)
            return terms

    #Gets the probability or the coefficient of the given term in the topic
    def getCoeff(self, topic, term):
        if self.model == "NMF":
            weights = []
            top_features = []
            tfidf_feature_names = self.tfidf_vectorizer.get_feature_names()
            for topic_idx, topicID in enumerate(self.H):
                if topic_idx == topic:
                    top_features_ind = topicID.argsort()[:-20 - 1:-1]
                    top_features = [tfidf_feature_names[i] for i in top_features_ind]
                    weights = topicID[top_features_ind]
            for coeff, terms in zip(weights, top_features):
                if terms == term:
                    return coeff
        else:
            topic = int(topic.split(" ")[-1])
            for terms in self.lda_model.show_topic(topic):
                if terms[0] == term:
                    return terms[1]

    #Shows all the topics found in training
    def showTopics(self):
        if self.model == "NMF":
            ret = []
            for topic_idx, topicID in enumerate(self.H):
                ret.append("Topic " + str(topic_idx))
            return ret
        else:
            topics = self.lda_model.print_topics()
            ret = []
            for topic in topics:
                ret.append("Topic " + str(topic[0]))
            return ret

    #Returns a flag to check what model is deployed at the moment
    def getModel(self):
        return self.model