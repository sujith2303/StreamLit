def eval_preds(actual,predicted,num_questions,question_type):
    score = 0
    if question_type=='Multiple Choice':
        pass
    elif question_type=='Blanks' or question_type=='True or False':
        for i in range(num_questions):
            # actual[i] = 'True' if actual[i]==':rainbow[True]' else 'False'
            score+= int(actual[i].strip() == predicted[i].strip())
    else:
        pass
    return score
