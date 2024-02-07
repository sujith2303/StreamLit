import streamlit as st
import numpy as np
# import cv2
from model import generate_questions
from evaluate import eval_preds
import extra_streamlit_components as stx
from utils import *
from PIL import Image
import cv2

def f(context,num_questions,question_type):
    submit = st.button('Submit',key = f"submit_text_button{question_type}")
    if submit:
        if question_type == 'Multiple Choice':
            questions,answers = generate_questions(context,num_questions,question_type)
            options,questions = preprocess_mcqs(questions)
            with st.form("my_form"):
                for i in range(num_questions):
                    st.radio(f'Question {i+1}):  {questions[i]}',[options[i][0],options[i][1],options[i][2],options[i][3]],index = None,key = f"{question_type}{i}")
                st.form_submit_button("Submit")
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
            with st.form("my_form"):
                for i in range(num_questions):
                    st.write(f'Question {i+1}):  {questions[i]}')
                    st.text_input('Answer',placeholder="Type Here!!!",max_chars=30,key = f"{question_type}{i}" )
                # print(st.session_state)
                st.form_submit_button("Submit")
        else:
            questions,answers = generate_questions(context,num_questions,question_type)
            st.session_state['questions'] = questions
            st.session_state['answers'] = answers
            with st.form("my_form"):
                for i in range(num_questions):
                    st.write(f'Question {i+1}):  {questions[i]}')
                    st.text_area('Answer',placeholder="Type Here!!!",key=f"{question_type}{i}",height=2)
                st.form_submit_button("Submit")
        
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


st.markdown("<h1 style='text-align: center; '>QuizBot.AI</h1>", unsafe_allow_html=True)

Question_Type = stx.tab_bar(data=[
    stx.TabBarItemData(id="Multiple Choice", title="Multiple Choice",description = ''),
    stx.TabBarItemData(id="Blanks", title="Blanks",description=""),
    stx.TabBarItemData(id="True or False", title="True or False",description = ''),
    stx.TabBarItemData(id="Essay", title="Essay",description = ""),
    stx.TabBarItemData(id="One Word", title="One Word",description=""),
    ])


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
                options,questions = preprocess_mcqs(questions)
                with st.form("my_form"):
                    for i in range(num_questions):
                        st.radio(f'Question {i+1}):  {questions[i]}',[options[i][0],options[i][1],options[i][2],options[i][3]],index = None,key = f"{question_type}{i}")
                    st.form_submit_button("Submit")
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
                with st.form("my_form"):
                    for i in range(num_questions):
                        st.write(f'Question {i+1}):  {questions[i]}')
                        st.text_input('Answer',placeholder="Type Here!!!",max_chars=30,key = f"{question_type}{i}" )
                    # print(st.session_state)
                    st.form_submit_button("Submit")
            else:
                questions,answers = generate_questions(context,num_questions,question_type)
                st.session_state['questions'] = questions
                st.session_state['answers'] = answers
                with st.form("my_form"):
                    for i in range(num_questions):
                        st.write(f'Question {i+1}):  {questions[i]}')
                        st.text_area('Answer',placeholder="Type Here!!!",key=f"{question_type}{i}",height=2)
                    st.form_submit_button("Submit")
            
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
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            context = text_detection(image)
            if context=="No Text Detected":
                st.warning('This image has no text. Please paste some other image', icon="⚠️")
                st.image(image)
            else:
                f(context,num_questions,question_type)
        

    elif TypeofInput=='Video':
        temp_video = st.file_uploader("Temp", type=["mp4", "avi", "mov"], key="temp")

        if temp_video is not None:
            with open(temp_video.name, "wb") as temp_file:
                temp_file.write(temp_video.getvalue())

            video_capture = cv2.VideoCapture(temp_video.name)
            fps = video_capture.get(cv2.CAP_PROP_FPS)
            duration = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT) / fps)
            st.write(f'The Video is :green[{duration}s] and has  :green[{fps*duration}] frames')
            st.write('Wait a moment......')
            if duration<10:
                # fps_to_extract =1
                frame_interval = int(1*fps)
            else:
                # fps_to_extract = 0.2
                frame_interval = int(duration//10 * fps)
            # frame_interval = int(fps / fps_to_extract)
            context = ''
            for frame_number in range(0, int(duration * fps), frame_interval):
  
                video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = video_capture.read()

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                res= text_detection(rgb_frame)
                if res!="No Text Detected":
                    context+=res
                # st.image(rgb_frame, caption=f"Frame at {frame_number // fps} seconds", use_column_width=True)

            video_capture.release()
            if context and len(context)>50:
                st.write(':upside_down_face: found this text inside your video.....')
                st.write(context)
                f(context,num_questions,question_type)
            elif len(context)<50:
                st.warning('Hmm.....Not enough text.Please choose other video!!!!')
            else:
                st.warning(":confounded: This video doesn't have any text.Please choose other video containing text", icon="⚠️")
                st.video(temp_video)
    else:
        pass       
                
initial_page_layout(Question_Type)
