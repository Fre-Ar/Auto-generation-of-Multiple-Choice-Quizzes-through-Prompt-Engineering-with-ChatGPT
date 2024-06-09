# -*- coding: utf-8 -*-
import json
import ipywidgets as widgets
from IPython.display import display, clear_output
from python.questionType import QuestionType

# Function to save quiz parameters
def saveQuizParameters(quizManager, filename):
    # Convert quizManager questions to a JSON serializable format
    data = {
        "questions": [q.__dict__ for q in quizManager.questions],
        "topicCoverage": quizManager.topicCoverage,
        "total": quizManager.total
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        print(f"Quiz parameters saved successfully to {filename}.")
    
# Function to load quiz parameters
def loadQuizParameters(quizManager, outputWidget, filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        quizManager.questions.clear()
        for questionData in data["questions"]:
            question = QuestionType(**questionData)
            quizManager.addQuestion(question)
        quizManager.topicCoverage = data["topicCoverage"]
        quizManager.total = data["total"]
        with outputWidget:
            clear_output()
            quizManager.show()

# Creates the Jupyter GUI to interact with (add, remove, list) the questions
def interactWithQuizManager(quizManager):
    
    # callback function for when the add button is clicked
    def addQuestion(button):
        with questionListOutput:
            clear_output()
            # creates a question type based on the values of the input
            question = QuestionType(int(countInput.value),
                        topicInput.value,
                        topicDescInput.value, 
                        goalInput.value,
                        difficultyInput.value,
                        int(nOptionsInput.value),
                        int(nCorrectInput.value))
            # adds that question to the quiz manager
            quizManager.addQuestion(question)
            #updates the index input
            indexInput.max=len(quizManager.questions)-1
            
            # updates the displayed list of questions
            quizManager.show()
        print("Question added successfully.")

    # callback function for when the remove button is clicked
    def removeQuestion(button):
        with questionListOutput:
            clear_output()
            try:
                # removes question type based on its index
                # (value of the index input)
                index = int(indexInput.value)
                quizManager.removeQuestion(index)
                #updates the index input
                indexInput.max=max(len(quizManager.questions)-1,0)
                print(f"Removed question at index {index}.")
            except ValueError:
                print("Please enter a valid integer for the question index.")
            except IndexError:
                print("Invalid index. Please enter a correct question index.")
            quizManager.show()
            
    # callback function for when the add button is clicked
    def addTopicCoverage(button):
        quizManager.topicCoverage.append(
                    (topicToCover.value,
                     percentageOfTopic.value))
        with questionListOutput:
            clear_output()
            # updates the displayed list of questions
            quizManager.show()

    # callback function for when the remove button is clicked
    def removeTopicCoverage(button):
        quizManager.topicCoverage.pop()
        with questionListOutput:
            clear_output()
            quizManager.show()
    
    #creates a visual output to display the list of question
    questionListOutput = widgets.Output()

    # style of the labels of the inputs
    st = {'description_width': 'initial'}
    #Titles
    questionLabel = widgets.Label(value="Question Specification")
    quizLabel = widgets.Label(value="Quiz Specification")
    # Inputs
    topicInput = widgets.Textarea(description="Topic:", style=st)
    topicDescInput = widgets.Textarea(description="Topic Description:",
                                          style=st)
    goalInput = widgets.Textarea(description="Goal/Learning Objective:", style=st)
    difficultyInput = widgets.Textarea(description="Difficulty for Target Demographic:", style=st)
    
    nOptionsInput = widgets.IntSlider(description="Number of options per question:",
                                      value=4,min=2,max=6, style=st)
    nCorrectInput = widgets.IntSlider(description="Number of correct options per question:",
                                      value=1,min=1,max=6, style=st)

    # Add button inputs
    countInput = widgets.IntSlider(min=1, max=20, value=1,
                                   description="Number of Questions to add:",
                                   style=st)
    addButton = widgets.Button(description="Add Question")
    addButton.on_click(addQuestion)

    # Remove button inputs
    indexInput = widgets.IntSlider(min=0, max=min(0,len(quizManager.questions)),
                                   value=0, description="Remove Index:", style=st)
    removeButton = widgets.Button(description="Remove Question")
    removeButton.on_click(removeQuestion)

    # Save and load parameter buttons 
    loadInput = widgets.Text(description="File to load from/save to:",
                             value="quizParameters.json", style=st)
    
    saveButton = widgets.Button(description="Save Parameters", style=st)
    saveButton.on_click(lambda b: saveQuizParameters(quizManager,
                                                     loadInput.value))
    
    loadButton = widgets.Button(description="Load Parameters", style=st)
    loadButton.on_click(lambda b: loadQuizParameters(quizManager, 
                                            questionListOutput, loadInput.value))
    
    topicToCover = widgets.Textarea(description="Topic to Cover:", style=st)
    percentageOfTopic = widgets.BoundedFloatText(description="Percentage Of Topic (from 0 to 1):", min=0, max=1.0, step=0.1, style=st)
    addTopicButton = widgets.Button(description="Add Topic Coverage", style=st)
    addTopicButton.on_click(addTopicCoverage)
    removeTopicButton = widgets.Button(description="Remove Topic Coverage", style=st)
    removeTopicButton.on_click(removeTopicCoverage)

    # layout of the GUI
    L = widgets.Layout(width='33%')
    inputColumn = widgets.VBox([questionLabel, topicInput, topicDescInput, 
                                goalInput, difficultyInput, nOptionsInput,
                           nCorrectInput], layout=L)  
    topicCoverageBox =  widgets.VBox([topicToCover, percentageOfTopic])  
    topicCoverageButtons =  widgets.HBox([addTopicButton, removeTopicButton])  
    actionColumn = widgets.VBox([countInput, addButton, indexInput, removeButton,
                                 topicCoverageBox, topicCoverageButtons,
                                 saveButton, loadInput, loadButton], layout=L)  
    displayColumn = widgets.VBox([quizLabel, questionListOutput], layout=L)
    layout = widgets.HBox([inputColumn, actionColumn, displayColumn])

    # display GUI
    display(layout)
    
