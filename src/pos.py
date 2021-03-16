import nltk

##POS Tagger used for Part of Speech tagging required for the window
class PosTagger:
    def __init__(self):
        print("POS Tagger: NLTK")

    #Return whether or not the given sentence contains any personal pronouns 
    def isPersonal(self, text):
        words = nltk.word_tokenize(text.lower())
        pos = nltk.pos_tag(words)
        for word in pos:
            if word[1] == "PRP" or word[1] == "PRP$":
                return True
        return False