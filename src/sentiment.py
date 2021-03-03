from textblob import TextBlob

##Sentiment model that is being used for the sentiment scores
class SentimentModel:
    def __init__(self):
        print("Sentiment Analyzer: textBlob")

    #Returns the sentiment score of the sentence provided as an argument
    def score(self, sentence):
        blob = TextBlob(sentence)
        return blob.sentiment