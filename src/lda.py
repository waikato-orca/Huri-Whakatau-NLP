from nltk.stem import PorterStemmer
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from utils import *

##LDA model that will be used for topic extraction
class LDAModel:
    def __init__(self, topicCollection):
        print("Topic Extraction Model: gensim.LDAModel")
        self.stemmer = PorterStemmer()

    #Train the LDA model on the current discussion
    def train(self, sentences):
        sentenceData = []
        for sentence in sentences:
            sentenceData.append(preprocess(sentence, self.stemmer))
        self.dictionary = Dictionary(sentenceData)
        bow_corpus = [self.dictionary.doc2bow(doc) for doc in sentenceData]
        self.lda_model = LdaModel(bow_corpus, num_topics=6, id2word=self.dictionary, passes=10)

    #Classify a given sentence to one of the topics found in training
    def classify(self, sentence):
        bow_vector = self.dictionary.doc2bow(preprocess(sentence, self.stemmer))
        return "Topic " + str(sorted(self.lda_model[bow_vector], key=lambda tup: -1*tup[1])[0][0])

    #Shows the terms of a given topic
    def showTerms(self, topic):
        terms = ""
        topic = int(topic.split(" ")[-1])
        for term in self.lda_model.show_topic(topic):
            terms += term[0] + ", "
        return terms

    #Gets the probability or the coefficient of the given term in the topic
    def getCoeff(self, topic, term):
        topic = int(topic.split(" ")[-1])
        for terms in self.lda_model.show_topic(topic):
            if terms[0] == term:
                return terms[1]

    #Shows all the topics found in training
    def showTopics(self):
        topics = self.lda_model.print_topics()
        ret = []
        for topic in topics:
            ret.append("Topic " + str(topic[0]))
        return ret

    #Returns a flag to check what model is deployed at the moment
    def getModel(self):
        return "LDA"