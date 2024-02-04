import streamlit as st
import numpy as np
# import cv2
from model import generate_questions
from evaluate import eval_preds


st.title("QuizBot.AI")

Multiple_Choice,Blanks,TrueorFalse,Essay,OneWord,Report_Card = st.tabs(['Multiple Choice','Blanks','True or False','Essay','OneWord','Report Card'])

# rad = st.sidebar.radio('Question Templates', ['Multiple Choice','Blanks','True or False','Essay','OneWord','Report Card'])

def initial_page_layout(question_type):
    if 'FormSubmitter:my_form-Submit' not in st.session_state:
        st.session_state['FormSubmitter:my_form-Submit'] = False
    left_column, right_column = st.columns(2)
    with left_column:
        TypeofInput = st.selectbox(
        'Choose input Type',
        ('Text', 'Video', 'Image','video link'),key=f'selectbox{question_type}'
        )
        
    with right_column:
        num_questions = st.slider('Num_Questions',min_value=1,max_value=10,key= f'slider{question_type}')
    
    if TypeofInput =='Text':
        context = st.text_area(label="Enter text",placeholder='StartTyping..',help = "Paste text from anywhere and generate Questions in seconds.....",key = f"text_area{question_type}")
        submit = st.button('Submit',key = f"submit_text_button{question_type}")
        if submit:
            if question_type == 'Multiple Choice':
                questions,answers = generate_questions(context,num_questions,question_type)
                st.text(questions+answers)
            elif question_type=='True or False':
                questions,answers = generate_questions(context,num_questions,question_type)
                st.session_state['questions'] = questions
                st.session_state['answers'] = answers
                with st.form("my_form"):
                    for i in range(num_questions):
                        st.radio(f'Question {i+1}):  {questions[i]}',['True','False'],index = None,key = f"{question_type}{i}")
                    # print(st.session_state)
                    st.form_submit_button("Submit")
            elif question_type=='Blanks':
                questions,answers = generate_questions(context,num_questions,question_type)
                st.session_state['questions'] = questions
                st.session_state['answers'] = answers
                print(answers)
                with st.form("my_form"):
                    for i in range(num_questions):
                        st.write(f'Question {i+1}):  {questions[i]}')
                        st.text_input('Answer',placeholder="Type Here!!!",max_chars=30,key = f"{question_type}{i}" )
                    # print(st.session_state)
                    st.form_submit_button("Submit")
            else:
                pass
        
            
        if st.session_state['FormSubmitter:my_form-Submit']:
    
            st.balloons()
            user_responses = []
            for i in range(num_questions):
                user_responses.append(st.session_state[f'{question_type}{i}'])
            score = eval_preds(st.session_state['answers'],user_responses,num_questions,question_type)
            if score/num_questions<0.36:
                st.progress(score/(num_questions+0.01),text  =":disappointed: You failed.Don't worry!! Retry!!")
                st.write(f'You Scored :red[{score}] out of {num_questions} ')
            else:
                st.progress(score/(num_questions+0.01),text  ="Congrats!! You passed :sunglasses: ")
                st.write(f'You Scored :blue[{score}] out of {num_questions} ')
            with st.expander("Feedback"):
                for i in range(num_questions):
                    text = f'Question {i+1}) :' + st.session_state['questions'][i]
                    actual_answer = st.session_state['answers'][i]
                    predicted_response = st.session_state[f'{question_type}{i}']
                    st.write(text)
                    st.write(f"Actual Response :{actual_answer}")
                    if actual_answer.strip() ==predicted_response:
                        st.write(f"Your Response  :blue[{predicted_response}]")
                    else:
                        st.write(f"Your Response  **:red[{predicted_response}]**")

    elif TypeofInput=='Image':
        pass
    elif TypeofInput=='Video':
        pass
    else:
        pass       
                


with Blanks:
    initial_page_layout('Blanks')
