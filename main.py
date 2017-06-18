from EPmail import EPmail
from BusquedasEPO import*
from BusquedasSem import*
import threading
from linkTypeform import*
from datetime import datetime
import calendar
import time



def main():
    ###Obtener resultados desde Typeform
    # name_id, mail_id, text_id = 'textfield_52850379',\
    #                             'email_52850524',\
    #                             'textarea_52850750'
    #
    # content = getFormComplete(offset=0, limit=5)
    #
    # nombre, mail, respuesta = getResponses(content=content, id=name_id),\
    #                           getResponses(content=content, id=mail_id), \
    #                           getResponses(content=content, id=text_id)
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
    text = 'cronometraje deportivo; sensores RFID; sensores activos; sensores ultrasonicos'
    data = 'client3'
    pn = None

    words = getWordsText(text)
    sent = sentenceProcessing(text)
    cql = preProcessing(sent,pn)
    createCSV(data)

    a = int(100.0/25.0)
    for k in range(a):
        client = initEPO()
        rbegin = (k)*40+1
        rend = (k+1)*40
        response = client.published_data_search(cql=cql,
                                            range_begin=rbegin,
                                            range_end=rend,
                                            constituents=None)
        #print(getSoup(response).prettify())
        country, number, kind = busquedaEPO(response, 'country', type='html'),\
                            busquedaEPO(response, 'doc-number', type='html'),\
                            busquedaEPO(response, 'kind', type='html')
        for i in range(len(country)):
            abstract = Abstract(client=client,
                                number=number[i],
                                country=country[i],
                                kind=kind[i])
            aux = country[i] + number[i] + kind[i]
            if abstract==None:
                pass
            else:
                writeCSV(data,getConcordance(words,abstract),aux,abstract)

    path = './'+data+'.csv'
    name = './'+data+'-sort.csv'
    sortCSV(path,name)

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


def multiSearch(client,country,number,kind,path,words):
    for i in range(len(country)):
        abstract = Abstract(client=client,
                            number=number[i],
                            country=country[i],
                            kind=kind[i])
        aux = country[i] + number[i] + kind[i]
        if abstract == None:
            pass
        else:
            writeCSV(path, getConcordance(words, abstract), aux, abstract)


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