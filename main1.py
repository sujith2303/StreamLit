
"""
with TrueorFalse:
    initial_page_layout('True or False')

with Blanks:
    initial_page_layout('Blanks')

with Essay:
    initial_page_layout('Essay')






if TypeofInput == 'Text':
    data = st.text_area(label="Enter text",placeholder='StartTyping..')
    submit = st.button('Submit')
    if submit:
        with Multiple_Choice:
            questions,answers = generate_questions(data,num_questions=num_questions,question_type='Multiple Choice')
            for i in range(num_questions):
                st.radio(f'Question{i+1} {questions[i]}',['A)','B)','C)','D)'])
                st.text(answers[i])
        with TrueorFalse:
            questions,answers = generate_questions(data,num_questions=num_questions,question_type='True or False')
            for i in range(num_questions):
                st.radio(f'Question{i+1}{questions[i]}',['True','False'])
elif TypeofInput == 'Image':
    uploaded_file = st.file_uploader(label="Choose an Image",type = ['png','jpg','jpeg'])
    if uploaded_file is not None:
        pass"""