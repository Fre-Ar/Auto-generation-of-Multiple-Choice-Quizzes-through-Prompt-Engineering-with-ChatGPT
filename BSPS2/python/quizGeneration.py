# -*- coding: utf-8 -*-

from openai import OpenAI
from openai.types.chat.completion_create_params import ResponseFormat


# sends prompt to the OpenAI API with the prompt from the promptBuilder
# and writes the .json file into the specified file.
# @params: 
# - promptBuild: a tuple (system prompt, user prompt)
# - fileNameToWrite: the name of the file into which to write the ChatGPT output
# - gptModel: the name of the gpt model (ex: "gpt-3.5-turbo-1106" or "gpt-4o")
def generateQuiz(promptBuild, fileNameToWrite, gptModel):
    client = OpenAI()
    # tell the API to output a valid JSON file as output
    responseFormat = ResponseFormat(type="json_object")
    
    completion = client.chat.completions.create(
    model=gptModel,
    response_format=responseFormat,
    messages=[
            {"role": "system", "content": promptBuild[0]},
            {"role": "user", "content": promptBuild[1]}
        ]
    )
    output = completion.choices[0].message
    content = output.content
    
    # write the output onto the specified file
    with open(fileNameToWrite, 'w', encoding="utf-8") as file:
        file.write(content)

def promptBuilderP0(quizManager):
    questions = quizManager.questions
    questionDescriptions = ';\n'.join([f"""-{q.nOccurences} questions each with exactly {q.nOptions} options, {q.nCorrect} of which are correct options, with the rest of the options being distractors. 
    They should be about {q.topic}, these should accomplish the following goal: {q.goal}. 
    These questions should be suitable for {q.difficulty} level in {q.topic}.""" for q in questions])
    
    systemPrompt = f"""Generate a multiple choice quiz based on the parameters given to you by the user.
        Your return should be the exact json structure of the following example (if there was 1 question with 3 options, another with 2 options, and a final one with 4 options):
    {{
    	"title": str,
    	"sectionOrderRandomized":boolean,
    	"sections": [
    		{{
    			"name": str,
    			"questionOrderRandomized":boolean,
    			"questions": [
    				{{
    					"context": str,
    					"question": str,
    					"points": float,
    					"optionOrderRandomized":boolean,
    					"options": [
    						{{
    							"option": str,
    							"correct": boolean,
    							"point": float,
    							"feedback": str
    						}},
    						{{
    							"option": str,
    							"correct": boolean,
    							"point": float,
    							"feedback": str
    						}},
    						{{
    							"option": str,
    							"correct": boolean,
    							"point": float,
    							"feedback": str
    						}}
    					]
    				}}
    			]
    		}},
    		{{
    			"name": str,
    			"questionOrderRandomized":boolean,
    			"questions": [
    				{{
    					"context": str,
    					"question": str,
    					"points": float,
    					"optionOrderRandomized":boolean,
    					"options": [
    						{{
    							"option": str,
    							"correct": boolean,
    							"point": float,
    							"feedback": str
    						}},
    						{{
    							"option": str,
    							"correct": boolean,
    							"point": float,
    							"feedback": str
    						}}
    					]
    				}}
    			]
    		}},
    		{{
    			"name": str,
    			"questionOrderRandomized":boolean,
    			"questions": [
    				{{
    					"context": str,
    					"question": str,
    					"points": float,
    					"optionOrderRandomized":boolean,
    					"options": [
    						{{
    							"option": str,
    							"correct": boolean,
    							"point": float,
    							"feedback": str
    						}},
    						{{
    							"option": str,
    							"correct": boolean,
    							"point": float,
    							"feedback": str
    						}},
    						{{
    							"option": str,
    							"correct": boolean,
    							"point": float,
    							"feedback": str
    						}},
    						{{
    							"option": str,
    							"correct": boolean,
    							"point": float,
    							"feedback": str
    						}}
    					]
    				}}
    			]
    		}}
    	]
    }}
        """
    
    userPrompt = f""" Generate a multiple choice quiz with {quizManager.total} total questions.
    The questions generated should be the following: {questionDescriptions} """
    return (systemPrompt, userPrompt)


# takes in a QuizMakerManager object (uses the P1 prompt)
def promptBuilder(quizManager):
    questions = quizManager.questions
    
    topicDescriptions = '\n'.join(["The topic of "+q.topic+" is described as "+q.topicDesc+"." for q in questions])
    questionDescriptions = ';\n'.join([f"""{q.nOccurences} questions each with exactly {q.nOptions} options, {q.nCorrect} of which are correct options, with the rest of the options being distractors. 
    They should be about {q.topic}, these should target the following goal: {q.goal}. 
    These questions should be suitable for {q.difficulty} level in {q.topic}.""" for q in questions])
    
    systemPrompt = f"""You are an expert quiz maker and especialist in {",".join([q.topic for q in questions])} for the purposes of learning support. 
    {topicDescriptions}
    
    Your task is focused on creating top quality multiple-choice question assessments. A multiple-choice question is a collection of three components (Stem, Correct Answers, Distractors), given a particular context of what the student is expected to know. The topic, as well as the context of the topic, will be provided in order to generate effective multiple-choice questions. 
    
    The stem refers to the question the student will attempt to answer, as well as the relevant context necessary in order to answer the question. It may be in the form of a question, an incomplete statement, or a scenario. The stem should focus on assessing the specific knowledge or concept the question aims to evaluate. 
    
    The Correct Answer(s) refers to the correct, undisputable answer(s) to the question in the stem. 
    
    A Distractor is an incorrect answer to the question in the stem and adheres to the following properties. 
    (1) A distractor should not be obviously wrong. In other words, it must still bear relations to the stem and correct answer. 
    (2) A distractor should be phrased positively and be a true statement that does not correctly answer the stem, all while giving no clues towards the correct answer. 
    (3) Although a distractor is incorrect, it must be plausible.
    (4) A distractor must be incorrect. It cannot be correct, or interpreted as correct by someone who strongly grasps the topic. 
    
    Use “None of the Above” or “All of the Above” style answer choices sparingly. These answer choices have been shown to, in general, be less effective at measuring or assessing student understanding. 
    
    Multiple-choice questions should be clear, concise, and grammatically correct statements. Make sure the questions are worded in a way that is easy to understand and does not introduce unnecessary complexity or ambiguity. Students should be able to understand the questions without confusion. The question should not be too long, and allow most students to finish in less than the given time. This means adhering to the following properties. 
    (1) Avoid using overly long sentences. 
    (2) If you refer to the same item or activity multiple times, use the same phrase each time. 
    (3) Ensure that each multiple-choice question provides full context. In other words, if a phrase or action is not part of the provided topic or topic context that a student is expected to know, then be sure to explain it briefly or consider not including it. 
    (4) Ensure that none of the distractors overlap. In other words, attempt to make each distractor reflect a different misconception on the topic, rather than a single one, if possible. 
    (5) Avoid too many clues. Do not include too many clues or hints in the answer options, which may make it too obvious for students to determine the correct answer. These options should require students to use their knowledge and reasoning to make an informed choice.
    
    Blooms’ Taxonomy and Action Verbs: 
    Multiple-choice questions must be well aligned to the learning objectives they are intended to assess students’ knowledge on. This implies that they must assess skills at the right cognitive level corresponding to the Bloom’s taxonomy categorization of the learning objective. Bloom’s Taxonomy offers a framework for categorizing the depth of learning, and it provides guidance on selecting appropriate action verbs when writing learning objectives. Here are the six levels of Bloom’s taxonomy and their definitions: 
    • Remember - This level involves retrieving, recognizing, and recalling relevant knowledge from long-term memory. 
    • Understand - At this level, learners construct meaning from oral, written, and graphic messages through interpreting, exemplifying, classifying, summarizing, inferring, comparing, and explaining. 
    • Apply - This level requires learners to carry out or use a procedure through executing or implementing it. 
    • Analyze - At this level, learners break material into constituent parts, determine how the parts relate to one another and to an overall structure or purpose through differentiating, organizing.
    • Evaluate - This level involves making judgments based on criteria and standards through checking and critiquing.
    • Create - At this level, learners put elements together to form a coherent or functional whole, or they reorganize elements into a new pattern or structure through generating.
    
    Difficulty levels:
    Multiple-choice questions must be obey certain rules to make sure the difficulty of the MCQ is appropriate:
    • Beginner - The question should be simple, the correct answer(s) should be obvious and the distractors should be easy to distinguish from the correct answer(s).
    • Intermediate - The question should be complicated, the correct answer(s) shouldn't pose too much of a problem to figure out but the distractors should make the student second guess their choices.
    • Advanced - The question should be complex, the correct answer(s) should be impossible to get right without good knowledge of the topic and the distractors should guessing impossible and disencourage uninformed choices.
    
    Output Format
    Output your multiple-choice quiz in an easy-to-parse json dictionary format. The quiz generated should have exactly {len(questions)} questions in total. 
    The questions generated should be the following:
    {questionDescriptions}
    
    Your return should be the exact json structure of the following example (if there was 1 question with 3 options, another with 2 options, and a final one with 4 options):
{{
	"title": str,
	"sectionOrderRandomized":boolean,
	"sections": [
		{{
			"name": str,
			"questionOrderRandomized":boolean,
			"questions": [
				{{
					"context": str,
					"question": str,
					"points": float,
					"optionOrderRandomized":boolean,
					"options": [
						{{
							"option": str,
							"correct": boolean,
							"point": float,
							"feedback": str
						}},
						{{
							"option": str,
							"correct": boolean,
							"point": float,
							"feedback": str
						}},
						{{
							"option": str,
							"correct": boolean,
							"point": float,
							"feedback": str
						}}
					]
				}}
			]
		}},
		{{
			"name": str,
			"questionOrderRandomized":boolean,
			"questions": [
				{{
					"context": str,
					"question": str,
					"points": float,
					"optionOrderRandomized":boolean,
					"options": [
						{{
							"option": str,
							"correct": boolean,
							"point": float,
							"feedback": str
						}},
						{{
							"option": str,
							"correct": boolean,
							"point": float,
							"feedback": str
						}}
					]
				}}
			]
		}},
		{{
			"name": str,
			"questionOrderRandomized":boolean,
			"questions": [
				{{
					"context": str,
					"question": str,
					"points": float,
					"optionOrderRandomized":boolean,
					"options": [
						{{
							"option": str,
							"correct": boolean,
							"point": float,
							"feedback": str
						}},
						{{
							"option": str,
							"correct": boolean,
							"point": float,
							"feedback": str
						}},
						{{
							"option": str,
							"correct": boolean,
							"point": float,
							"feedback": str
						}},
						{{
							"option": str,
							"correct": boolean,
							"point": float,
							"feedback": str
						}}
					]
				}}
			]
		}}
	]
}}


    
    Below are some examples:
    Example 1 (
    - 2 questions each with exactly 4 options, 1 of which are correct options, with the rest of the options being distractors. 
    They should be about Generative AI and LLMs, these should target the following learning objective: Teaching about the topic, not testing knowledge of skills. 
    These questions should also be at the Remember level in Bloom’s taxonomy, and should be suitable for Beginner level in Generative AI and LLMs, specially for adults who have little to no knowledge about technologies and AI and should not take more than 1 minute to answer.;
    - 1 questions each with exactly 4 options, 2 of which are correct options, with the rest of the options being distractors. 
    They should be about Generative AI and LLMs, these should target the following learning objective: Teaching about the topic, not testing knowledge of skills. 
    These questions should also be at the Remember level in Bloom’s taxonomy, and should be suitable for Beginner level in Generative AI and LLMs, specially for adults who have little to no knowledge about technologies and AI and should not take more than 1 minute to answer.) : 
    
{{
	"title": "MCQ about AI for Beginner's",
	"sectionOrderRandomized":false,
	"sections":[
		{{
			"name":"General Concepts",
			"questionOrderRandomized":false,
			"questions": [
				{{
					"context": "AI, GPT, and LLM are often used interchangeably nowadays.",
					"question": "What does \"LLM\" stand for in the context of AI?",
					"points":1,
					"optionOrderRandomized":false,
					"options": 
						[
							{{
								"option": "Large Language Model",
								"correct": true,
								"point":1,
								"feedback": "LLMs are trained on huge sets of data, so they are \"large\". They are a computer program trying to immitate (or \"model\") human \"language\" generation and processing."
							}},
							{{
								"option": "Long Local Machine",
								"correct": false,
								"point":0,
								"feedback": "Good try, but while LLMs are a piece of technology, they are not physical machines."
							}},
							{{
								"option": "Long-term Learning Module",
								"correct": false,
								"point":0,
								"feedback": "Good try, LLMs do indeed learn and are planned to last do so continuously for a long time, what distinguises LLMs is their size and natural language capabilities."
							}},
							{{
								"option": "Limited Liability Management",
								"correct": false,
								"point":0,
								"feedback": "Fortunately, AIs and LLMs have nothing to do with coorporate companies... for now."
							}}						
						]
				}},
				{{
					"context":"",
					"question": "Which of the following is an example of Generative AI's capabilities?",
					"points":1,
					"optionOrderRandomized":false,
					"options": 
						[
							{{
								"option": "Generating a news article based on a headline.",
								"correct": true,
								"point":0.5,
								"feedback": "Generative AI can analyze the context and content implied by a headline and then produce a comprehensive news article that aligns with the style, tone, and factual requirements suggested by that headline. This capability demonstrates its ability to understand and generate contextually relevant text."
							}},
							{{
								"option": "Creating realistic video game environment art.",
								"correct": true,
								"point":0.5,
								"feedback": "Generative AI can learn from vast amounts of data on landscapes, architectural styles, and environmental elements to create new, realistic video game environments. This process involves understanding the principles of design and environmental coherence to generate visually appealing and contextually suitable game worlds."
							}},
							{{
								"option": "Solving mathematical equations.",
								"correct": false,
								"point":0,
								"feedback": " Solving mathematical equations typically involves computational and algorithmic approaches rather than generative processes. Generative AI focuses on creating new content based on learned patterns rather than solving structured, rule-based problems."
							}},
							{{
								"option": "Running physical simulations for engineering projects.",
								"correct": false,
								"point":0,
								"feedback": "Running physical simulations involves computational models that predict how physical systems behave under various conditions, which is more about calculation and analysis rather than generating new, creative content. This task is typically handled by specialized simulation software, not generative AI."
							}}	
						]
				}}
			]
		}},
		{{
			"name":"AI responsability",
			"questionOrderRandomized":false,
			"questions": [
				{{
					"context": "There's been a lot of talk in the media about the impact of using Generative AI in nefarious ways.",
					"question": "Why is it important to use Generative AI responsibly?",
					"points":1,
					"optionOrderRandomized":false,
					"options": 
						[
							{{
								"option": "To avoid spreading misinformation.",
								"correct": true,
								"point":1,
								"feedback": "Generative AI models can generate convincing text that could be mistaken for factual information, so it's important to fact check anything generated by AIs!"
							}},
							{{
								"option": "To ensure it does not replace human jobs.",
								"correct": false,
								"point":0,
								"feedback": "While concerns about AI and automation affecting employment exist, the primary reason for using Generative AI responsibly is not specifically about job replacement. It's more about ethical use, accuracy, and the potential impact on society, such as spreading misinformation or ethical concerns in its applications."
							}},
							{{
								"option": "To make sure it can only play video games.",
								"correct": false,
								"point":0,
								"feedback": "The scope of Generative AI extends far beyond just playing video games. The importance of using Generative AI responsibly relates to its broader applications, including content creation, decision-making support, and more. The focus on responsible use is about preventing misuse and ensuring ethical considerations in its diverse applications, not limiting it to entertainment purposes."
							}},
							{{
								"option": "To prevent it from becoming too powerful.",
								"correct": false,
								"point":0,
								"feedback": "The notion of AI becoming \"too powerful\" is a speculative and sci-fi scenario. The concern in the real world focuses on ensuring that AI is developed and used in ways that are ethical, fair, and do not harm society, rather than a fear of AI gaining autonomous power or control."
							}}					
						]
				}}
			]
		}}	
	]
}}

    Example 2 (
    - 2 questions each with exactly 3 options, 1 of which are correct options, with the rest of the options being distractors. 
    They should be about French History during the Napoleonic Wars, these should target the following learning objective: Testing basic french history knowledge. 
    These questions should also be at the Remember level in Bloom’s taxonomy, and should be suitable for Intermediate level in French History during the Napoleonic Wars, specially for high school students who have studied a history class chapter on French History and should not take more than 1 minute to answer.;
    - 1 questions each with exactly 3 options, 1 of which are correct options, with the rest of the options being distractors. 
    They should be about women in french history, these should target the following learning objective: Teach about important french female historical figures.
    These questions should also be at the Understand level in Bloom’s taxonomy, and should be suitable for Beginner level in women in french history, specially for high school students who have studied a history class chapter on French History and should not take more than 1 minute to answer.) : 
    - 1 questions each with exactly 3 options, 1 of which are correct options, with the rest of the options being distractors. 
    They should be about historical French landmarks, these should target the following learning objective: Test knowledge about the eiffel tower and other french monuments.
    These questions should also be at the Understand level in Bloom’s taxonomy, and should be suitable for Beginner level in historical French landmarks, specially for high school students who have studied a history class chapter on French History and should not take more than 1 minute to answer.) : 

{{
	"title": "French History: Napoleon and other historical figures",
	"sectionOrderRandomized":false,
	"sections":[
		{{
			"name":"Napoleonic France",
			"questionOrderRandomized":false,
			"questions": [
				{{
					"context": "",
					"question": "Which battle was Napoleon I's final defeat?",
					"points":2,
					"optionOrderRandomized":false,
					"options": 
						[
							{{
								"option": "Battle of Waterloo",
								"correct": true,
								"point":2,
								"feedback": "The Battle of Waterloo (June 18, 1815) was Napoleon I's final defeat, ending 23 years of recurrent warfare between France and the other powers of Europe. It was fought between Napoleon's 72,000 troops and the combined forces of the duke of Wellington's allied army of 68,000 (with British, Dutch, Belgian, and German units) and about 45,000 Prussians, the main force of Gebhard Leberecht von Blücher's command. Four days later Napoleon abdicated for the second time."
							}},
							{{
								"option": "Battle of Agincourt",
								"correct": false,
								"point":0,
								"feedback": "The Battle of Agincourt took place on October 25, 1415, and was a major English victory over the French in the Hundred Years' War. This battle occurred nearly 400 years before Napoleon I's time and is notable for the use of the English longbow, which decimated the French knights and nobility. This makes it unrelated to Napoleon I's military campaigns and final defeat."
							}},
							{{
								"option": "Battle of Verdun",
								"correct": false,
								"point":0,
								"feedback": "The Battle of Verdun, fought from February to December 1916 during World War I, was one of the longest and most devastating battles in world history. It involved French and German forces in a brutal conflict with enormous casualties on both sides. Since this battle took place nearly a century after Napoleon I's death, it could not represent his final defeat."
							}}						
						]
				}},
				{{
					"context": "",
					"question": "What French author's father was a general for Napoleon and was nicknamed \"the Black Devil\"?",
					"points":2,
					"optionOrderRandomized":false,
					"options": 
						[
							{{
								"option": "Alexandre Dumas",
								"correct": true,
								"point":2,
								"feedback": "Alexandre Dumas is well known for classics like The Three Musketeers, but his father Thomas-Alexandre Dumas was famous in his own right. The child of an enslaved Haitian and a white Frenchman, the elder Dumas joined the French army, rose through the ranks, and became France’s first Black general. The author Dumas is said to have based some of the action in his novels on his father’s exploits."
							}},
							{{
								"option": "Victor Hugo",
								"correct": false,
								"point":0,
								"feedback": "Victor Hugo, the illustrious author of Les Misérables and The Hunchback of Notre-Dame, had a father who served as a high-ranking officer under Napoleon. However, Hugo's father, Joseph Léopold Sigisbert Hugo, was not known as \"the Black Devil.\" Instead, Hugo's works often reflect his complex views on society, justice, and humanity, rather than direct inspiration from his father's military career. This distinguishes him from Alexandre Dumas, whose father's legendary military exploits directly influenced his storytelling."
							}},
							{{
								"option": "Albert Camus",
								"correct": false,
								"point":0,
								"feedback": "Albert Camus, a philosopher and writer known for his contributions to absurdism and existentialism, was born in Algeria to a French-Algerian (Pied-Noir) family. His father, Lucien Camus, died in World War I, long after Napoleon's era, and had no historical ties to Napoleon's military campaigns. Camus is celebrated for works like The Stranger and The Plague, which explore the human condition and morality, unrelated to the Napoleonic military legacy."
							}}						
						]
				}}
			]
		}},
		{{
			"name":"French Women",
			"questionOrderRandomized":false,
			"questions": [
				{{
					"context": "",
					"question": "Which of these French women was charged with the crime of wearing men's clothing?",
					"points":1,
					"optionOrderRandomized":false,
					"options": 
						[
							{{
								"option": "Joan of Arc",
								"correct": true,
								"point":1,
								"feedback": "Joan of Arc was a peasant girl who became a great military leader for France, defeating the English at Orléans in 1429. Unfortunately, she ran afoul of religious authorities by claiming God spoke directly to her (undermining the church) and wearing men’s clothing. She was convicted of heresy and burned at the stake. Decades later the conviction was overturned. In the 20th century she was made a saint."
							}},
							{{
								"option": "Marie-Antoinette",
								"correct": false,
								"point":0,
								"feedback": "Marie-Antoinette, the last Queen of France before the French Revolution, was known for her extravagant lifestyle and the famous misquote \"Let them eat cake.\" However, she was never charged with the crime of wearing men’s clothing. Her charges during her trial in 1793 were related to treason, depletion of the national treasury, and conspiracy against the security of the state, not her attire. This makes her an incorrect choice for this question."
							}},
							{{
								"option": "Marie Curie",
								"correct": false,
								"point":0,
								"feedback": "Marie Curie was a renowned physicist and chemist, famous for her research on radioactivity and as the first woman to win a Nobel Prize. At no point was Marie Curie charged with the crime of wearing men’s clothing. Her professional and personal life was scrutinized for her scientific contributions and personal relationships, not her fashion choices."
							}}						
						]
				}}
			]
		}},
		{{
			"name":"French landmarks",
			"questionOrderRandomized":false,
			"questions": [
				{{
					"context":"",
					"question": "Which of these French landmarks was designed to be taken down after 20 years?",
					"points":1,
					"optionOrderRandomized":false,
					"options": 
						[
							{{
								"option": "Eiffel Tower.",
								"correct": true,
								"point":1,
								"feedback": "The Eiffel Tower was constructed for the International Exposition of 1889. Paris gave Gustave Eiffel use of the land the tower stood on for 20 years. Fortunately, the structure was able to prove its usefulness as an antenna in the blossoming field of radio, and in 1910 the lease was renewed for 70 years."
							}},
							{{
								"option": "Louvre Museum.",
								"correct": false,
								"point":0,
								"feedback": "Originally a 12th-century fortress, the Louvre was never intended to be temporary. It evolved into a world-renowned museum, housing iconic art like the Mona Lisa, showcasing its permanent significance in French heritage."
							}},
							{{
								"option": "Arc de Triomphe.",
								"correct": false,
								"point":0,
								"feedback": "Commissioned by Napoleon to honor military achievements, the Arc de Triomphe was completed in 1836 and designed as a permanent monument, not a temporary structure."
							}}	
						]
				}}
			]
		}}
	]	
}}
    
    """  

    userPrompt = f"""Generate a top quality quiz with {len(questions)} multiple-choice questions that follow this:
    {questionDescriptions}
    """
    
    return (systemPrompt, userPrompt)



