from EPmail import EPmail
from BusquedasEPO import*
from BusquedasSem import*
from linkTypeform import*


def main():

#####################################
# Obtener resultados desde Typeform #

    name_id, mail_id, text_id = 'textfield_52850379', 'email_52850524', 'textarea_52850750'
    content = getFormComplete(offset=5, limit=5)

    status = json.loads(content)["http_status"]
    #HTTPstatus(status=status)


    nombre, mail, respuesta = getResponses(content=content, id=name_id),\
                              getResponses(content=content, id=mail_id),\
                              getResponses(content=content, id=text_id)
    #print(nombre[0]), print(mail[0]), print(respuesta[0])


# Extraer palabras claves de la "respuesta"

#    for i in range(len(respuesta)):
#        text = respuesta[i]
#        text = limpiarRespuesta(text=text)
#        print(text)

# Buscar "respuesta" en la EPO      #

    cql = 'ti=' + 'gun' + ' prox ' + 'ti=' + 'machine'
    #cql = 'ab=explosive'


    client = initEPO()
    response = client.published_data_search(cql= cql,
                                            range_begin=1,
                                            range_end=25,
                                            constituents=None)
    #print(getSoup(response).prettify())


    country, number, kind = busquedaEPO(response, 'country', type='html'),\
                            busquedaEPO(response, 'doc-number', type='html'),\
                            busquedaEPO(response, 'kind', type='html')
    #print(country), print(number), print(kind)


    for i in range(len(country)):
        #response = abstract_helper(client=client,
        #                           number=number[i],
        #                           country=country[i],
        #                           kind=kind[i])
        #print(getSoup(response, type='xml').prettify())

        abstract = Abstract(client=client,
                            number=number[i],
                            country=country[i],
                            kind=kind[i])
        print(abstract)


def limpiarRespuesta(text):
    text = translateText('es', 'en', text)
    text = deletePunt(text)
    text = deleteStop('spanish', text)
    text = deleteWord('PRP', text)
    text = deleteWord('PRP$', text)
    text = deleteWord('IN', text)
    text = deleteWord('DT', text)
    return stemmingLemmatizer(text=text)


def Abstract(client, number, country, kind):
    response = abstract_helper(client, number, country, kind)
    abstract = busquedaLang(response, idioma='en', type='xml')
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