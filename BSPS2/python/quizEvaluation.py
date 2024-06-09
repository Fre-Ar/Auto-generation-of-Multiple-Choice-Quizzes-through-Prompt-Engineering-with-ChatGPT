
from openai import OpenAI
from re import search, sub
from python.quizMakerManager import QuizManager
from python.questionType import QuestionType

testSuite = [
    (1, [(0.7, "Trivia")], 
        [(1, "Trivia: General Knowledge", "have fun with general knowledge", "easy for everyone", 3, 1)]),
    (1, [(1, "Philosophy: Existentialism")], 
        [(1, "Philosophy: Existentialism", "understand existential philosophy", "hard for college students", 4, 2)]),
    (2, [(0.5, "Biology"), (0.2, "Environmental Science")], 
        [(1, "Biology: Cell Structure", "understand cell structure", "medium for high school students", 3, 2), 
         (1, "Environmental Science: Climate Change", "raise awareness about climate change", "medium for adults", 5, 1)]),
    (2, [(0.7, "Cooking"), (0.5, "Nutrition")], 
        [(1, "Cooking", "learn basic cooking techniques", "easy for beginners", 4, 1),
         (1, "Nutrition", "understand nutritional information", "medium for all ages", 4, 1)]),
    (3, [(0.3, "Ethics"), (0.5, "Philosophy"), (0.4, "Logic")], 
        [(1, "Ethics", "understand basic ethical principles", "medium for college students", 3, 1),
         (1, "Philosophy", "test knowledge of philosophical theories", "hard for college students", 4, 1),
         (1, "Logic", "learn logical reasoning", "medium for high school students", 2, 1)]),
    (4, [(0.7, "Chemistry"), (0.5, "Physics")], 
        [(3, "Chemistry: Reactions", "test knowledge of chemical reactions", "hard for college students", 5, 2), 
         (1, "Physics: Optics", "understand basic optics principles", "medium for high school students", 5, 1)]),
    (4, [(0.4, "Art")], 
        [(2, "Art History", "learn about art movements", "medium for art students", 5, 1),
         (2, "Modern Art", "understand modern art concepts", "hard for general audience", 4, 1)]),
    (5, [(0.2, "Geography"), (0.3, "History")], 
        [(1, "Geography: Climate Zones", "identify different climate zones", "medium for middle school students", 4, 1),
         (1, "Geography: Deserts", "identify major world deserts", "easy for high school students", 3, 1), 
         (1, "History: Ancient Civilizations", "learn about ancient civilizations", "medium for middle school students", 4, 1), 
         (1, "History: Industrial Revolution", "understand the Industrial Revolution", "medium for high school students", 4, 1), 
         (1, "History: World War II", "understand key events of WWII", "medium for high school students", 5, 1)]),
    (6, [(0.5, "Pharmacology"), (0.3, "Microbiology"), (0.2, "Medical Ethics")], 
        [(3, "Pharmacology", "know the basics of drug classifications", "medium for medical students", 4, 1),
         (2, "Microbiology", "understand microorganisms and their effects", "medium for medical students", 5, 1),
         (1, "Medical Ethics", "grasp ethical issues in healthcare", "easy for healthcare professionals", 3, 1)]),
    (7, [(0.4, "Calculus"), (0.7, "Statistics")], 
        [(4, "Calculus: Derivatives", "practice derivative calculation", "medium for college students", 4, 1), 
         (3, "Statistics: Probability", "understand basic probability concepts", "easy for college students", 6, 2)])
]


def QuizFromTestSuite(suite):
    total = 0
    qM = QuizManager()
    qM.topicCoverage = suite[1]
    for q in suite[2]:
        total += q[0]
        qType = QuestionType(q[0], q[1], "", q[2], q[3], q[4], q[5])
        qM.questions.append(qType)
    qM.total = total
    if total != suite[0]:
        return None
    return qM




def evaluateTOrG(quizManager, quizData, i, j, model, topicOrGoal="topic"):
    try:
        sys = f"""You are an expert in the evaluation of the coherence of a question with respect to a quiz's {topicOrGoal}.
For each request the user is sending you, you are given:
- a quiz {topicOrGoal} description
- a question 
You have to output the coherence level of the question with respect to the quiz according to the following scale:
1 if the question is related to the the core aspects of the {topicOrGoal}
0.75 if the question is related to the core aspects but also peripheral aspects
0.5 if the question is equally related to the core aspects and non core aspects
0.25 if the question mainly diverges from the core aspects
0 doesn’t address the core aspects at all

Explain your thought process.
Write the result between {{}}.
Do not use latex in your answer."""
        tOrG = quizManager.questions[i].topic if topicOrGoal == "topic" else quizManager.questions[i].goal
        user = f"""
    {topicOrGoal}: 
    {tOrG}

    Question:
    {quizData["sections"][i]["questions"][j]["context"]}
    {quizData["sections"][i]["questions"][j]["question"]}
    {quizData["sections"][i]["questions"][j]["options"]}
    """
    except:
        return 0
      
    promptBuild = (sys,user)
    content = generatePrompt(promptBuild, model)
    content = sub(r'\\.*?\\', '', content)
    score = search("{(.*)}", content)
    while(score == None):
        content = generatePrompt(promptBuild, model)
        score = search("{(.*)}", content)
    score = score.group(1)
    print(topicOrGoal, "score:", score)
    return float(sub("[^\d\.]", "", score))

def evaluateDifficulty(quizManager, quizData, i, j, model):
    try:
        sys = f"""You are an expert in the evaluation of the coherence of a question with respect to a quiz's difficulty for a given demographic of quiz takers.
For each request the user is sending you, you are given:
- a quiz difficulty description with respect to a demographic
- a question 
You have to output the coherence level of the question with respect to the quiz according to the following scale:
1 if the question's difficulty matches the quiz difficulty for the specified demographic
0.75 if the difficulty partially matches
0.5 if the question equally matches the difficulty as much as it doesn't match
0.25 if the question is mainly of a different difficulty for the specified demographic
0 if the question is nowhere near matching the specified difficulty for the specified demographic

Explain your thought process.
Write the result (which is a number from 0 and 1) between {{}}.
Do not use latex in your answer."""
        user = f"""
    Difficulty: 
    {quizManager.questions[i].difficulty}

    Question
    {quizData["sections"][i]["questions"][j]["context"]}
    {quizData["sections"][i]["questions"][j]["question"]}
    {quizData["sections"][i]["questions"][j]["options"]}
    """
    except:
        return 0
    promptBuild = (sys,user)
    content = generatePrompt(promptBuild, model)
    content = sub(r'\\.*?\\', '', content)
    score = search("{(.*)}", content)
    while(score == None):
        content = generatePrompt(promptBuild, model)
        score = search("{(.*)}", content)
    score = score.group(1)
    print("dif score: ", score)
    return float(sub("[^\d\.]", "", score))

def evaluateOptions(quizManager, quizData, i, j):
    try:
        x1 = quizManager.questions[i].nOptions
        y1 = len(quizData["sections"][i]["questions"][j]["options"])
        x2 = quizManager.questions[i].nCorrect
        y2 = len([o for o in quizData["sections"][i]["questions"][j]["options"] if o["correct"]])
    except:
        return 0,0
    
    print("P(Op)", x1,"G(Op)", y1,"P(CoOp)", x2,"G(CoOp)", y2)
    print("respect(Op): ", dis(x1,y1), "respect(CoOp)", dis(x2,y2))
    return dis(x1,y1),dis(x2,y2)
   
def evaluateTopicCoverage(quizManager, quizData, model):
    total = 0
    sys = f"""You are an expert in the evaluation of the topic coverage of a given quiz with respect to a topic.
For each request the user is sending you, you are given:
- a topic
- a quiz
You have to output the percentage of the material of the topic that the quiz covers. 
For example, a quiz about only vectors and inner products covers a small percentage of the "Linear Algebra 1" topic but covers a larger percentage of the topic "Inner Product Spaces"

Explain your thought process.
Write the result (which is a number from 0 and 1) between {{}}.
Do not use latex in your answer."""
    for topicCover in quizManager.topicCoverage:
        user = f"""
        Topic: 
        {topicCover[1]}

        Quiz:
        {showQuiz(quizData)}
        """
        promptBuild = (sys,user)
        content = generatePrompt(promptBuild, model)
        content = sub(r'\\.*?\\', '', content)
        score = search("{(.*)}", content)
        while(score == None):
            content = generatePrompt(promptBuild, model)
            score = search("{(.*)}", content)
        score = score.group(1)
        score = sub("[^\d\.]", "", score)
        score = dis(float(score), topicCover[0])
        print(topicCover[1], score)
        total += score
    
    print("topic Coverage: ", total/len(quizManager.topicCoverage))
    return total/len(quizManager.topicCoverage)

def evaluateQuiz(quizManager, quizData, model, storage):
    storage["global"] = 0
    storage["format"] = 1
    glob = dis(quizManager.total, sum([len(s["questions"]) for s in quizData["sections"]]))
    storage["nQuestions"] = glob
    glob += 1
    tCscore = evaluateTopicCoverage(quizManager, quizData, model)
    storage["topicCoverage"] = tCscore
    glob += tCscore
    glob /= 3
    storage["global"] = glob
    loc = 0
    storage["questions"] = []
    nQuestions = 0
    for i in range(len(quizManager.questions)):
        for j in range(quizManager.questions[i].nOccurences):
            storage["questions"].append({})
            
            topic =  evaluateTOrG(quizManager, quizData, i, j, model, "topic")
            goal =  evaluateTOrG(quizManager, quizData, i, j, model, "goal")
            dif = evaluateDifficulty(quizManager, quizData, i, j, model)
            op, cOp = evaluateOptions(quizManager, quizData, i, j)
            qTotal = (topic+goal+dif+op+cOp)/5
            
            storage["questions"][-1]["topic"] = topic
            storage["questions"][-1]["goal"] =  goal
            storage["questions"][-1]["difficulty"] = dif
            storage["questions"][-1]["nOptions"] = op
            storage["questions"][-1]["nCorrectOptions"] = cOp
            storage["questions"][-1]["question"] = qTotal
            
            loc += qTotal
            
        nQuestions += quizManager.questions[i].nOccurences
    loc/=nQuestions
    storage["local"] = loc
    storage["total"] = (glob+loc)/2
    print(storage)
    
    print("Total score: ")
    return (glob+loc)/2

    
    
def generatePrompt(promptBuild, gptModel):
    client = OpenAI()
    # tell the API to output a valid JSON file as output
   # responseFormat = ResponseFormat(type="json_object")
    
    completion = client.chat.completions.create(
    model=gptModel,
    #response_format=responseFormat,
    messages=[
            {"role": "system", "content": promptBuild[0]},
            {"role": "user", "content": promptBuild[1]}
        ]
    )
    print("done")
    output = completion.choices[0].message
    print(output.content)
    return str(output.content)
    
def dis(x,y):
    if(min(x,y)==0):
        return 0
    return 1/(1+abs(x-y)/min(x,y))

def showQuiz(qData):
    quiz = ""
    for s in qData["sections"]:
        for q in s["questions"]:
            quiz += q["question"]
            quiz += "\n"
            for o in q["options"]:
                quiz += o["option"]
                quiz += "("+str(o["correct"])+")\n"
                #quiz += "feedback: " + o["feedback"] + "\n"
            quiz += "\n"
    return quiz

