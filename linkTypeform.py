from bs4 import BeautifulSoup
import typeform


def initType(typeform_UID = 'BdzCUz', apikey = 'a4b5f45414ebad1defbb80651a961ef09e364e82'):
    return typeform.Form(api_key=apikey, form_id=typeform_UID)


def getAnswer(answers, question_id='terms_52851375'):
    aux = getResponseForm(answers)
    if question_id in aux:
        return aux.split(question_id, 1)[-1]
    else:
        return None

def getResponseForm(answer):
    return '{question_id}{answer}'.format(question_id=answer.question_id, answer=answer.answer)

def getResponseList(response,name_id,mail_id,text_id):
    aux = ['','','']
    for answer in response.answers:
        if(getAnswer(answer,name_id)!=None): aux[0] = getAnswer(answer,name_id)
        if(getAnswer(answer,mail_id)!=None): aux[1] = getAnswer(answer,mail_id)
        if(getAnswer(answer,text_id)!=None): aux[2] = getAnswer(answer,text_id)
    return aux