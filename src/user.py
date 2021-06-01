##User object that stores the username and other required counts throughout the discussion
class User:
    def __init__(self, name):
        self.name = name
        self.questionCount = 0
        self.pronounCount = 0
        self.turnCount = 0
        self.wordCount = 0
        self.firstPos = [0.00, 0.00, 0.00]
        self.finalPos = [0.00, 0.00, 0.00]
        self.semJump = 0
        self.shift = 0
        self.topics = []
        self.lastResponse = [0.00, 0.00, 0.00]

    #Resets all the counts of the given user to 0
    def resetCounts(self):
        self.questionCount = 0
        self.pronounCount = 0
        self.turnCount = 0
        self.wordCount = 0