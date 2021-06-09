from EPmail import EPmail
# from BusquedasEPO import*
from BusquedasSem import *
# import threading
from linkTypeform import *
from datetime import datetime
import calendar
import time


def main():
    count = 0
    data = './client.csv'
    text = 'panel solar; fotovoltaico; estructura modular'
    pn = None
    path = data + str(count)
    words = getWordsText(text)
    sent = sentenceProcessing(text)
    cql = preProcessing(sent, pn)

    #searchResponse(path, cql, words)
    client = initEPO()
    rbegin = 1
    rend = 40
    response = client.published_data_search(cql=cql,
                                            range_begin=rbegin,
                                            range_end=rend,
                                            constituents=None)
    # print(getSoup(response).prettify())
    country, number, kind = busquedaEPO(response, 'country', type='html'), \
                            busquedaEPO(response, 'doc-number', type='html'), \
                            busquedaEPO(response, 'kind', type='html')
    for i in range(len(country)):
        title = Title(client=client,
                      number=number[i],
                      country=country[i],
                      kind=kind[i])
        aux = country[i] + number[i] + kind[i]
        if title != None:
            writeCSV(data, getConcordancev2(words, title), aux, title)


def Abstract(client, number, country, kind):
    response = abstract_helper(client, number, country, kind)
    # if abstract == None:
    #      aux = busquedaLang(response, idioma='ol', type='xml')
    #      #abstract = translateTextAuto(lengout='en',text=str(aux))
    #      abstract = translateText(aux)
    return busquedaLang(response, idioma='en', type='xml')


def abstract_helper(client, number, country, kind):
    return client.published_data(
        reference_type='publication',
        input=epo_ops.models.Docdb(str(number), country, kind),
        endpoint='abstract',
    )


def title_helper(client, number, country, kind):
    return client.published_data(
        reference_type='publication',
        input=epo_ops.models.Docdb(str(number), country, kind),
        endpoint='title',
    )


def Title(client, number, country, kind):
    response = title_helper(client, number, country, kind)
    return busquedaLang(response, idioma='en', type='xml')


def HTTPstatus(status):
    s = ""
    if status == 200:
        s = "Everything worked as expected"
    elif status == 400:
        s = "Invalid date in query/"
    elif status == 403:
        s = "Expired Token/Invalid Token/Token does not have access permissions/Invalid Token"
    elif status == 404:
        s = "Type in URL/Invalid typeform ID"
    elif status == 429:
        s = "Request limit reached"
    return print("http_status = " + s)


def searchResponse(data, cql, words):
    createCSV(data)
    a = int(100.0 / 25.0)
    for k in range(a):
        client = initEPO()
        rbegin = (k) * 40 + 1
        rend = (k + 1) * 40
        response = client.published_data_search(cql=cql,
                                                range_begin=rbegin,
                                                range_end=rend,
                                                constituents=None)
        # print(getSoup(response).prettify())
        country, number, kind = busquedaEPO(response, 'country', type='html'), \
                                busquedaEPO(response, 'doc-number', type='html'), \
                                busquedaEPO(response, 'kind', type='html')
        for i in range(len(country)):
            abstract = Abstract(client=client,
                                number=number[i],
                                country=country[i],
                                kind=kind[i])
            aux = country[i] + number[i] + kind[i]
            if abstract != None:
                writeCSV(data, getConcordancev2(words, abstract), aux,
                         abstract)

    path = './' + data + '.csv'
    name = './' + data + '-sort.csv'
    sortCSV(path, name)


if __name__ == "__main__":
    main()
