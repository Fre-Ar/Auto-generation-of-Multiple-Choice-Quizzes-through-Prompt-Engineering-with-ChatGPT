# -*- coding: utf-8 -*-

import random
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import json

# Loads quiz data
def loadQuiz(filename):
    # Open file with UTF-8 encoding to ensure character compatibility
    with open(filename, 'r', encoding="utf-8") as file:
        # Return the loaded JSON data as a Python dictionary
        return json.load(file)

# Displays the quiz dictionary with Jupyter widgets
# and displays feeeback upon submission
def displayQuiz(quizData):
    # Create a submit button for the quiz
    submitButton = widgets.Button(description="Submit Quiz")
    # Create output widgets for displaying sections and feedback
    sectionsOutput = widgets.Output()
    feedbackOutput = widgets.Output()
    
    # List of widgets for all sections
    sectionsWidgets = []
    # Initialize total points available in the quiz
    totalPointsPossible = 0
    
    # Handle section randomization if specified
    sections = quizData['sections']
    if quizData['sectionOrderRandomized']:
        random.shuffle(sections)
    
    # Prepare each section in the quiz
    for section in sections:
        ### create the section, question and option text 
        ### create the CheckBox widgets for each option
        
        ### display the section, question and option text
        ### create CheckBox widgets for each option and display them
        
        # List of widgets for the questions in this section
        sectionQuestionsWidgets = []
        # Initialize points available in this section
        sectionPointsPossible = 0
        with sectionsOutput:
            # Output the section name as an HTML header
            display(HTML(f"<h2>Section: {section['name']}</h2>"))
            # Access and potentially randomize the order of questions
            questions = section['questions']
            if section['questionOrderRandomized']:
                random.shuffle(questions)
            # Process each question in the section
            for question in questions:
                # Add the question points to both totals
                sectionPointsPossible += question['points']
                totalPointsPossible += question['points']
                # Display the context, question text and points of the question
                print(question['context'])
                print(question['question'] + f" (Points: {question['points']})")
                # Randomize option order if specified
                options = question['options']
                if question['optionOrderRandomized']:
                    random.shuffle(options)
                # Create a checkbox widget for each option
                optionWidgets = [widgets.Checkbox(description=option['option'],
                                                  value=False, indent=False)
                                for option in options]
                # add widget to widget list
                sectionQuestionsWidgets.append((optionWidgets, options, 
                                                question['question'],
                                                question['points']))
                # display the option widgets
                for option in optionWidgets:
                    display(option)
        # add the group of widgets for this section to the larger section widgets list
        sectionsWidgets.append((sectionQuestionsWidgets, sectionPointsPossible,
                                section['name']))
        
    # callback function when the submit button is pressed
    # displays the feedback based on the chosen options
    def onSubmit(b):                                                    
        
        # Function to handle quiz submission, calculate scores and show feedback
        with feedbackOutput:
            clear_output()
            # Initialization of feedback text container and total earned score
            feedbackHtml = ""
            totalScoreEarned = 0
            # Evaluate each section separately
            for sectionQuestions, sectionPoints, sectionName in sectionsWidgets:
                ## add total feedback to the feedback text (feedbackHtml)
                ## add option points to the total score
                
                # Initialization of score earned this section
                sectionScoreEarned = 0
                # Add section title to the feedback container
                feedbackHtml += f"<h3>{sectionName}</h3>"
                # for each question widget
                for questionWidgets, questionData, questionText, questionPoints in sectionQuestions:
                    questionScore = 0
                    feedbackHtml += f"<div><strong>{questionText}</strong> (Points: {questionPoints})</div>"
                    # for each option widget
                    for optionWidget, optionData in zip(questionWidgets, questionData):
                        # if selected
                        if optionWidget.value:
                            # and was correct
                            if optionData['correct']:
                                # display green text and add score
                                feedbackHtml += f"""<div style='color: green;
                                font-weight: bold;'>Selected: {optionData['option']}
                                - Feedback: {optionData['feedback']}</div>"""
                                questionScore += optionData['point']
                            # and was wrong
                            else:
                                # display red text and add score
                                feedbackHtml += f"""<div style='color: red;
                                font-weight: bold;'>Selected: {optionData['option']}
                                - Feedback: {optionData['feedback']}</div>"""
                                questionScore += optionData['point']
                        # if not selected and was correct
                        elif optionData['correct']:
                            # display orange text
                            feedbackHtml += f"""<div style='color: orange;
                            font-weight: bold;'>Missed: {optionData['option']}
                            - Feedback: {optionData['feedback']}</div>"""
                    # display score for the question
                    feedbackHtml += f"<div>Scored {questionScore}/{questionPoints}</div>"
                    # add score to total earned
                    sectionScoreEarned += questionScore
                # display score for the section
                feedbackHtml += f"""<div><strong>Total {sectionName}
                    Score: {sectionScoreEarned}/{sectionPoints}</strong></div>"""
                # add score to total earned
                totalScoreEarned += sectionScoreEarned
            # Display total score for the entire quiz
            feedbackHtml += f"""<h2>Total Quiz Score: {totalScoreEarned}/{totalPointsPossible}
                        or {totalScoreEarned/totalPointsPossible*100:.2f}%</h2>"""
            # Display the feedback text
            display(HTML(feedbackHtml))
            # Disable the quiz
            submitButton.disabled = True
            for sectionQuestions, _, _ in sectionsWidgets:
                for options, _, _, _ in sectionQuestions:
                    for option in options:
                        option.disabled = True
    # Link the submit button to the onSubmit function
    submitButton.on_click(onSubmit)
    # Display all elements
    display(sectionsOutput)
    display(submitButton)
    display(feedbackOutput)


