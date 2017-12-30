import json
import urllib.request


typeform_UID = ''
apikey = ''


def getFormComplete(typeform_UID = typeform_UID,
                    apikey = apikey,
                    since=None,     #since tiempo unix desde cuando quiero los resultados del formulario
                    until=None,     #until tiempo unix hasta cuando quiero los resultados del formulario
                    offset=None,    #offset entrega resultados desde el numero indicado en offset
                    limit=None,     #limit muestra los resultados indicados en limit desde el resultado indicado en offset
                    token=None,     #token entrega el formulario especificado por el token
                    orden_by='data_sumit'): #orden_by data especifica el orden
    url = "https://api.typeform.com/v1/form/" + typeform_UID + "?" + "key=" + apikey +\
          "&" + "completed=true" + "&" + "order_by[]="+orden_by
    if since!=None:
        url = url+'&since='+str(since)
    if until!=None:
        url = url+'&until='+str(until)
    if offset!=None:
        url = url+'&offset='+str(offset)
    if limit!=None:
        url = url+'&limit='+str(limit)
    if token!=None:
        url = url+'&token='+str(token)

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


def getResponses(content, id):
    obj = json.loads(content)
    showing = obj['stats']['responses']['showing']
    aux = list()
    for i in range(showing):
        aux2 = obj['responses'][i]['answers'][id]
        aux.append(aux2)
    return aux
