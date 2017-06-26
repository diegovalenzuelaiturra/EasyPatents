from EPmail import EPmail
#from BusquedasEPO import*
from BusquedasSem import*
#import threading
from linkTypeform import*
from datetime import datetime
import calendar
import time



def main():
    ###Obtener resultados desde Typeform
    name_id, mail_id, text_id = 'textfield_QClJ','email_i7FN','textarea_LyO0'
                                #'textfield_52850379','email_52850524','textarea_52850750'
    #

    #bus = list()

    ##enaex
    #text = 'emulsion explosiva; explosivo plástico; aceite con agua; emulsificante; robusto'
    #data = 'client1'
    #pn='WO' #solo patentes internacionales

    ##Paper wallet
    #text = 'metodo billetera plegable; billetera de papel;hoja rectangular sin cortes'
    #data = 'client2'
    #pn = None

    ##Timer cronos
    #text = 'cronometraje deportivo; sensores RFID; sensores activos; sensores ultrasonicos'

    itext = "Hola! soy Ro, y respondo a lo que solicitaste usando las palabras ["
    ftext =  """           
Cualquier duda por favor contacta a uno de nuestros humanos
dvalenzuela@easypatents.cl es uno de los mejores que conozco.
            
Que tengas un buen dia!"""
    ferror = "Lo siento, pero tus criterios no arrojan resultados."

    msubject = 'Busqueda EasyPatents'
    mfrom = 'ribanez@easypatents.cl'
    data = 'client'
    pn = 'WO'

    d = datetime.utcnow()
    timestamp1 = str(calendar.timegm(d.utctimetuple()))
    count = 0
    while (True):
        d = datetime.utcnow()
        timestamp2 = str(calendar.timegm(d.utctimetuple()))
        if timestamp1 == '':
            content = getFormComplete(typeform_UID='RWKyVl', until=timestamp1)
        else:
            content = getFormComplete(typeform_UID='RWKyVl', since=timestamp1)
        timestamp1 = timestamp2
        # Hay que hacer la subrutina para responder los correos
        # content = getFormComplete(typeform_UID='RWKyVl',offset=0, limit=5)
        #
        #print(content)
        nombre, mail, respuesta = getResponses(content=content, id=name_id),\
                                  getResponses(content=content, id=mail_id), \
                                  getResponses(content=content, id=text_id)

        where = 'ab'
        for k in range(len(respuesta)):
            path = data+str(count)
            words = getWordsText(respuesta[k])
            sent = sentenceProcessing(respuesta[k])
            print(sent)
            cql = preProcessing(where, sent, pn)
            print(cql)

            gamma = 0.01
            searchResponse(path, cql, words, gamma)
            epm = EPmail()
            fname = './'+path+'-sort.csv'
            fformat = 'resp.csv'
            mmessage = itext + respuesta[k]+' ] '+ftext
            aux = epm.send_complex_message(mail[k],mfrom,msubject,mmessage,fformat,fname)
            print(mail[k])
            print(aux)
            count+=1
                # epm = EPmail()
                # mmessage = itext + respuesta[k]+' ] '+ferror+ftext
                # aux = epm.send_simple_message(mail[k],mfrom, msubject,mmessage)
                # print(mail[k])
                # print(aux)
        time.sleep(60)


def Abstract(client, number, country, kind):
    response = abstract_helper(client, number, country, kind)
    abstract = busquedaLang(response, idioma='en', type='xml')
    # if abstract == None:
    #      aux = busquedaLang(response, idioma='ol', type='xml')
    #      #abstract = translateTextAuto(lengout='en',text=str(aux))
    #      abstract = translateText(aux)
    return abstract


def abstract_helper(client, number, country, kind):
    response = client.published_data(reference_type='publication',
                                     input=epo_ops.models.Docdb(str(number), country, kind),
                                     endpoint='abstract',
                                     )
    return response


def HTTPstatus(status):
    s = ""
    if status == 200:
        s = "Everything worked as expected"
    if status == 400:
        s = "Invalid date in query/"
    if status == 403:
        s = "Expired Token/Invalid Token/Token does not have access permissions/Invalid Token"
    if status == 404:
        s = "Type in URL/Invalid typeform ID"
    if status == 429:
        s = "Request limit reached"
    return print("http_status = " + s)


def searchResponse(data,cql,words,gamma):
    createCSV(data)
    a = int(200/25.0)
    for k in range(a):
        client = initEPO()
        rbegin = (k)*25+1
        rend = (k+1)*25
        #try:
        response = client.published_data_search(cql=cql,
                                            range_begin=rbegin,
                                            range_end=rend,
                                            constituents=None)
        #except:
        #print("error en la respuesta epo cql incorrecta")
        #print(getSoup(response).prettify())
        #try:
        country, number, kind = busquedaEPO(response, 'country', type='html'),\
                            busquedaEPO(response, 'doc-number', type='html'),\
                            busquedaEPO(response, 'kind', type='html')
        #except:
        #print("error en la respuesta epo numero de publicacion incorrecta")
        for i in range(len(country)):
            abstract = Abstract(client=client,
                                number=number[i],
                                country=country[i],
                                kind=kind[i])
            aux = country[i] + number[i] + kind[i]
            if abstract==None:
                pass
            else:
                writeCSV(data,Score(words,abstract,gamma),aux,abstract)

    path = './'+data+'.csv'
    name = './'+data+'-sort.csv'
    sortCSV(path,name)


if __name__ == "__main__":
    main()


# from https://www.typeform.com/help/data-api/
# HTTP status code summary
    #  status
        # 200
            # Everything worked as expected
        # 400
            # Invalid date in query/
        # 403
            # Expired Token/Invalid Token/Token does not have access permissions/Invalid Token
        # 404
            # Type in URL/Invalid typeform ID
        # 429
            # Request limit reached

# from https://pypi.python.org/pypi/python-epo-ops-client
    # When you issue a request, the response is a requests.Response object
        # If response.status_code != 200 then a requests.HTTPError exception will be raised

    # The following custom exceptions are raised for cases when OPS quotas are exceeded,
    # they are all in the epo_ops.exceptions module and are subclasses of requests.HTTPError,
    # and therefore offer the same behaviors:
        # IndividualQuotaPerHourExceeded
        # RegisteredQuotaPerWeekExceeded