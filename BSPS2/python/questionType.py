# Class representing a type of question
class QuestionType:
    def __init__(self, nOccurences, topic, topicDesc, goal,
                 difficulty, nOptions, nCorrect):
        self.nOccurences = nOccurences
        self.topic = topic
        self.topicDesc = topicDesc
        self.goal = goal
        self.difficulty = difficulty
        self.nOptions = nOptions
        self.nCorrect = nCorrect
        
    def __repr__(self):
        return f"""Question Type(Occurences: {self.nOccurences},
                Topic: {self.topic}, Goal: {self.goal},
                Difficulty: {self.difficulty}, 
                Options: {self.nOptions}, Correct: {self.nCorrect})"""

    def equals(self, question):
        # Check if all attributes are equal
        return (
            self.topic == question.topic and
            self.topicDesc == question.topicDesc and
            self.goal == question.goal and
            self.difficulty == question.difficulty and
            self.nOptions == question.nOptions and
            self.nCorrect == question.nCorrect
        )
    
    
    
    