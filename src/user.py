##User object that stores the username and other required counts throughout the discussion
class User:
    def __init__(self, name):
        self.name = name
        self.questionCount = 0
        self.pronounCount = 0

    #Resets all the counts of the given user to 0
    def resetCounts(self):
        self.questionCount = 0
        self.pronounCount = 0