# -*- coding: utf-8 -*-

from python.questionType import QuestionType

# Class that contains and manages the quiz/question specifications
class QuizManager:
    def __init__(self):
        self.questions = []
        self.topicCoverage = []
        self.total = 0

    # adds a question specification to the list of questions
    def addQuestion(self, question):
        self.total += question.nOccurences
        for q in self.questions:
            if question.equals(q):
                q.nOccurences += question.nOccurences
                return
        self.questions.append(question)

    # removes a question specification from the list
    # of questions at position index
    def removeQuestion(self, index):
        if index < len(self.questions):
            self.total -= self.questions[index].nOccurences
            del self.questions[index]
        else:
            print("Invalid question index.")

    # lists all the added question specifications
    def listQuestions(self):
        for idx, question in enumerate(self.questions):
            print(f"{idx}: {question}")
    
    # lists all the added topic coverage tuples
    def listTopicCoverage(self):
        for topic in self.topicCoverage:
            print(f"{topic[1]} of {topic[0]}")

    # lists the quiz specification
    def show(self):
        print("Quiz Specification")
        self.listTopicCoverage()
        print("Question Specification")
        self.listQuestions()


