from transformers import AutoModelForSeq2SeqLM,AutoTokenizer
import torch
from utils import *

def load_model_question():
    model_name = 'Sujithanumala/QuizBot.AI-base'
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model,tokenizer

def generate_questions(context,num_questions,question_type):
    model,tokenizer = load_model_question()
    instruction = ''
    if question_type=='Multiple Choice':
        instruction = ' \n  Generate MCQS'
    elif question_type =='Blanks':
        instruction = ' \n Generate FIBs'
    elif question_type =='True or False':
        instruction = '\n Generate True or False'   
    else:
        instruction = ' \n Generate Essay answers'
    print(instruction)
    questions = []
    answers = []
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    model.to(device)
    predictions = model.generate(tokenizer(context+instruction,return_tensors='pt').to(device)['input_ids'],max_length = 100,num_beams = 10,num_return_sequences=num_questions)
    for i in predictions:
        result = tokenizer.decode(i,skip_special_tokens=True)
        # print(result)
        result = result.split('[ANSWER]:')
        # print(result)
        question,answer = result
        question = question.split('[QUESTION]: ')[1]
        questions.append(question)
        answers.append(answer)
    return questions,answers

if __name__=="__main__":
    questions,answers = generate_questions(context="In the late 19th century with the discovery of the electron, and in the early 20th century, with the discovery of the atomic nucleus, and the birth of particle physics, matter was seen as made up of electrons, protons and neutrons interacting to form atoms. Today, we know that even protons and neutrons are not indivisible, they can be divided into quarks, while electrons are part of a particle family called leptons. Both quarks and leptons are elementary particles, and are currently seen as being the fundamental constituents of matter",num_questions=1,question_type='True or False')
    print(questions,answers)
    for i in questions:
        print(i)
    print(preprocess_mcqs(questions))
