from wordcloud import WordCloud, STOPWORDS
from nltk.stem import PorterStemmer
from utils import *

##WordCloud model to show the significant words mentioned in the discussion
class CloudModel:
    def __init__(self):
        print("WordCloud Model: wordcloud")
        self.stemmer = PorterStemmer()

    #Generates the word cloud for the provided sentence
    def generate(self, sentence):
        cloud_sent = preprocess(sentence, self.stemmer)
        sent = ""
        for word in cloud_sent:
            sent += word + " "
        return WordCloud(max_words=25, stopwords= STOPWORDS).generate(sent)

    #Generates the word cloud for a list of sentences
    def batchGenerate(self, list):
        sent = ""
        for sentence in list:
            cloud_sent = preprocess(sentence, self.stemmer)
            for word in cloud_sent:
                sent += word + " "
        return WordCloud(max_words=25, stopwords= STOPWORDS).generate(sent)