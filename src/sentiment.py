from textblob import TextBlob
import pandas
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

##Sentiment model that is being used for the sentiment scores
class SentimentModel:
    def __init__(self, string):
        if string.lower() == "vader":
            self.model = "vader"
            print("Sentiment Analyzer: Vader")
            self.analyzer = SentimentIntensityAnalyzer()
        else:
            self.model = "textblob"
            print("Sentiment Analyzer: textBlob")

    #Returns the sentiment score of the sentence provided as an argument
    def score(self, sentence):
        if self.model == "vader":
            score = self.analyzer.polarity_scores(sentence)
            return score
        else:
            blob = TextBlob(sentence)
            return blob.sentiment