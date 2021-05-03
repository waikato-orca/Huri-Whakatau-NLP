import stanza
from stanza.server import CoreNLPClient

##Question model that is being used for question detection
class QuestionModel:
    def __init__(self):
        self.client = CoreNLPClient(annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref'], timeout=30000, memory='16G', threads= 1)

    #Returns whether or not the provided sentence contains any questions
    def isQuestion(self, text):
        ann = self.client.annotate(text)
        sentence = ann.sentence[0]
        constituency_parse = sentence.parseTree
        for child in constituency_parse.child:
            if child.value == "SQ" or child.value == "SBARQ":
                return True
        return False