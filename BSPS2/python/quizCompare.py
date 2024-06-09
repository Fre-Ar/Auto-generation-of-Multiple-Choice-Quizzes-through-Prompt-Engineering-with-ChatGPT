# -*- coding: utf-8 -*-

import json
import ipywidgets as widgets
from IPython.display import display, HTML

def loadQuizData(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def displayQuizzesSideBySide(quiz1, quiz2):
    # Load quiz data from files
    quizData1 = loadQuizData(quiz1)
    quizData2 = loadQuizData(quiz2)
    
    # Create widgets for each quiz
    quiz1Output = widgets.Output()
    quiz2Output = widgets.Output()
    
    with quiz1Output:
        print("Quiz 1")
        displayOneQuiz(quizData1)
    with quiz2Output:
        print("Quiz 2")
        displayOneQuiz(quizData2)
    
    # Display quizzes side by side using HBox
    hbox = widgets.HBox([quiz1Output, quiz2Output])
    display(hbox)

def displayOneQuiz(quizData):
    # Iterate through each section in the quiz
    for section in quizData['sections']:
        display(HTML(f"<h3>{section['name']}</h3>"))
        # Iterate through each question in the section
        for question in section['questions']:
            display(HTML(f"<strong>Question: {question['question']}</strong> ({question['points']} points)"))
            display(HTML(f"<em>Context: {question['context']}</em>"))
            # Display options and highlight correct ones
            options_html = "<ul>"
            for option in question['options']:
                color = "green" if option['correct'] else "black"
                options_html += f"<li style='color: {color};'>{option['option']} ({option['point']} points)</li>"
            options_html += "</ul>"
            display(HTML(options_html))



