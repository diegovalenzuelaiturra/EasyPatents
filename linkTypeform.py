import json
import urllib.request


def getFormComplete(typeform_UID = 'BdzCUz', apikey = 'a4b5f45414ebad1defbb80651a961ef09e364e82'):
    url = "https://api.typeform.com/v1/form/" + typeform_UID + "?" + "key=" + apikey +\
          "&" + "completed=true" + "&" + "order_by[]=date_submit,desc"  # + "&" + "limit=10"
    page = urllib.request.urlopen(url)
    return page.read().decode('utf8')


def getResponseList(content, name_id, mail_id, text_id):
    obj = json.loads(content)
    showing = obj['stats']['responses']['showing']
    aux = list()
    for i in range(showing):
        aux2 = ['','','']
        aux2[0] = obj['responses'][i]['answers'][name_id]
        aux2[1] = obj['responses'][i]['answers'][mail_id]
        aux2[2] = obj['responses'][i]['answers'][text_id]
        aux.append(aux2)
    return aux