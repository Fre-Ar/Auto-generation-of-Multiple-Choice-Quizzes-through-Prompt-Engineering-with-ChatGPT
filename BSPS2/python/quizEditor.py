import json
import ipywidgets as widgets
from IPython.display import display

# Function to load quiz data
def loadQuiz(filename):
    # Open file with UTF-8 encoding to ensure character compatibility
    with open(filename, 'r', encoding="utf-8") as file:
        # Return the loaded JSON data as a Python dictionary
        return json.load(file)

# Function to save quiz data
def saveQuiz(quizData, filename='editedQuiz.json'):
    # Open file for writing; will overwrite existing or create new
    with open(filename, 'w') as file:
        # Serialize quizData into JSON format with indentation for readability
        json.dump(quizData, file, indent=4)
        # Print confirmation message to the user
        print(f"Quiz saved successfully to {filename}.")

# Display and edit the quiz structure
def editQuiz(quizData):
    # Create text input widget for quiz title with initial value set from quizData
    quizTitle = widgets.Text(value=quizData['title'], description='Quiz Title:')
    # Checkbox to toggle whether section order should be randomized
    sectionOrderRandomizedCheckbox = widgets.Checkbox(value=quizData['sectionOrderRandomized'], description='Randomize Section Order')
    # Button to save the changes made to the quiz structure
    saveButton = widgets.Button(description="Save Changes", button_style='success')

    # Function to update quiz title in quizData when text input changes
    def updateTitle(change):
        quizData['title'] = change['new']
    
    # Function to update section order randomization setting in quizData when checkbox toggled
    def updateSectionOrderRandomized(change):
        quizData['sectionOrderRandomized'] = change['new']
    
    # Function to save quiz when save button is clicked
    def onSaveButtonClick(b):
        saveQuiz(quizData)
    
    # Attach change listeners to widgets
    quizTitle.observe(updateTitle, names='value')
    sectionOrderRandomizedCheckbox.observe(updateSectionOrderRandomized, names='value')
    saveButton.on_click(onSaveButtonClick)

    # Create an accordion widget to organize sections dynamically
    sectionAccordion = widgets.Accordion()
    # Generate a section editor widget for each section and store them in the accordion
    sections = [createSectionEditor(section, quizData['sections'], sectionAccordion) for section in quizData['sections']]
    sectionAccordion.children = sections
    
    # Set accordion titles for each section
    for i, section in enumerate(quizData['sections']):
        sectionAccordion.set_title(i, section['name'])
    
    # Button to add new sections to the quiz
    addSectionBtn = widgets.Button(description="Add New Section")
    
    # Function to add a new section to the quizData and accordion
    def addSection(b):
        newSection = {
            "name": "New Section",
            "questionOrderRandomized": False,
            "questions": []
        }
        quizData['sections'].append(newSection)
        new_section_widget = createSectionEditor(newSection, quizData['sections'], sectionAccordion)
        sectionAccordion.children = tuple(list(sectionAccordion.children) + [new_section_widget])
        sectionAccordion.set_title(len(sectionAccordion.children) - 1, newSection['name'])
    
    # Attach click event handler to the add section button
    addSectionBtn.on_click(addSection)
    
    # Display the entire interface including the quiz title, randomization checkbox, sections, and add section button
    display(widgets.VBox([quizTitle, sectionOrderRandomizedCheckbox, sectionAccordion, addSectionBtn, saveButton]))



def createSectionEditor(section, sections, accordion):
    nameInput = widgets.Textarea(value=section['name'],
                                 description='Section Name:')
    randomizeQuestions = widgets.Checkbox(
        value=section['questionOrderRandomized'],
        description='Randomize Question Order')
    questionsVBox = widgets.VBox(
        [createQuestionEditor(
            question, section['questions'])
            for question in section['questions']])
    addQuestionBtn = widgets.Button(description="Add New Question")
    removeSectionBtn = widgets.Button(
        description="Remove This Section",
        button_style='danger')
    
    def updateName(change):
        section['name'] = change['new']
        accordion.set_title(sections.index(section), section['name'])  # Update accordion title dynamically
    
    def updateRandomization(change):
        section['questionOrderRandomized'] = change['new']
    
    def addQuestion(b):
        newQuestion = {
            "context": "New Context",
            "question": "New Question",
            "points": 1.0,
            "optionOrderRandomized": False,
            "options": []
        }
        section['questions'].append(newQuestion)
        questionsVBox.children = tuple(
            list(questionsVBox.children) +
            [createQuestionEditor(newQuestion, section['questions'])])
    
    def removeSection(b):
        sections.remove(section)
        # Update the accordion display
        section_widgets = list(accordion.children)
        del section_widgets[sections.index(section)]
        accordion.children = tuple(section_widgets)
    
    nameInput.observe(updateName, names='value')
    randomizeQuestions.observe(updateRandomization, names='value')
    addQuestionBtn.on_click(addQuestion)
    removeSectionBtn.on_click(removeSection)
    
    return widgets.VBox([nameInput, randomizeQuestions, questionsVBox, addQuestionBtn, removeSectionBtn])

def createQuestionEditor(question, questions):
    contextInput = widgets.Textarea(value=question['context'], description='Context:')
    questionInput = widgets.Textarea(value=question['question'], description='Question:')
    pointsInput = widgets.FloatText(value=question['points'], description='Points:')
    optionOrderRandomizedCheckbox = widgets.Checkbox(value=question['optionOrderRandomized'], description='Randomize Option Order')
    optionsVBox = widgets.VBox([createOptionEditor(option, question['options']) for option in question['options']])
    addOptionBtn = widgets.Button(description="Add New Option")
    removeQuestionBtn = widgets.Button(description="Remove This Question", button_style='danger')
    
    def updateContext(change):
        question['context'] = change['new']
    
    def updateQuestion(change):
        question['question'] = change['new']
    
    def updatePoints(change):
        question['points'] = change['new']
    
    def updateOptionOrderRandomized(change):
        question['optionOrderRandomized'] = change['new']
    
    def addOption(b):
        newOption = {
            "option": "New Option",
            "correct": False,
            "point": 0.0,
            "feedback": "New Feedback"
        }
        question['options'].append(newOption)
        optionsVBox.children = tuple(list(optionsVBox.children) + [createOptionEditor(newOption, question['options'])])
    
    def removeQuestion(b):
        questions.remove(question)
        # Remove the whole question widget from the display
        question_widgets = list(optionsVBox.parent.children)
        del question_widgets[question_widgets.index(optionsVBox.parent)]
        optionsVBox.parent.parent.children = tuple(question_widgets)
    
    contextInput.observe(updateContext, names='value')
    questionInput.observe(updateQuestion, names='value')
    pointsInput.observe(updatePoints, names='value')
    optionOrderRandomizedCheckbox.observe(updateOptionOrderRandomized, names='value')
    addOptionBtn.on_click(addOption)
    removeQuestionBtn.on_click(removeQuestion)
    
    return widgets.VBox([contextInput, questionInput, pointsInput, optionOrderRandomizedCheckbox, optionsVBox, addOptionBtn, removeQuestionBtn])

def createOptionEditor(option, options):
    optionInput = widgets.Textarea(value=option['option'], description='Option:')
    correctCheckbox = widgets.Checkbox(value=option['correct'], description='Correct?')
    pointInput = widgets.FloatText(value=option['point'], description='Point Value:')
    feedbackInput = widgets.Textarea(value=option['feedback'], description='Feedback:')
    removeOptionBtn = widgets.Button(description="Remove This Option", button_style='danger')
    
    def updateOption(change):
        option['option'] = change['new']
    
    def updateCorrect(change):
        option['correct'] = change['new']
    
    def updatePoint(change):
        option['point'] = change['new']
    
    def updateFeedback(change):
        option['feedback'] = change['new']
    
    def removeOption(b):
        options.remove(option)
        # Remove the option widget from the display
        option_widgets = list(removeOptionBtn.parent.children)
        del option_widgets[option_widgets.index(removeOptionBtn.parent)]
        removeOptionBtn.parent.parent.children = tuple(option_widgets)
    
    optionInput.observe(updateOption, names='value')
    correctCheckbox.observe(updateCorrect, names='value')
    pointInput.observe(updatePoint, names='value')
    feedbackInput.observe(updateFeedback, names='value')
    removeOptionBtn.on_click(removeOption)
    
    return widgets.VBox([optionInput, correctCheckbox, pointInput, feedbackInput, removeOptionBtn])
