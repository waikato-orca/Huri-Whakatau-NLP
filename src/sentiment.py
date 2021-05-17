from textblob import TextBlob
# import pandas
# import matplotlib.pyplot as plt
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

##Sentiment model that is being used for the sentiment scores
class SentimentModel:
    def __init__(self):
        print("Sentiment Analyzer: textBlob")
        # print("Sentiment Analyzer: Vader")
        # self.analyzer = SentimentIntensityAnalyzer()

    #Returns the sentiment score of the sentence provided as an argument
    def score(self, sentence):
        blob = TextBlob(sentence)
        return blob.sentiment
        # score = self.analyzer.polarity_scores(sentence)
        # return score