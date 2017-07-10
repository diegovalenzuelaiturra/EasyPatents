from bs4 import BeautifulSoup
import epo_ops
import xmltodict, json
from Codigos import*


def busquedaEPO(response, elemento='abstract', type='html'):
    fin = list()
    if type=='html':
        soup = getSoup(response,'html.parser')
        aux = soup.find_all(elemento)
        for i in aux:
            fin.append(i.string)
        return fin
    elif type=='xml':
        soup = getSoup(response,'xml')
        aux = soup.find_all(elemento)
        for i in aux:
            fin.append(i.p.string)
        return fin
    else:
        return fin


def busquedaLang(response, idioma='en',type='xml'):
    #fin = list()
    soup = getSoup(response, type)
    aux = soup.find(lang=idioma)
    if aux != None:
        return aux.p.string
    else:
        return None


def publicNumber(country,number):
    aux = list()
    for i in range(len(country)):
        aux.append(str(country[i])+str(number[i]))
    return aux


def getSoup(response,type='html.parser'):
    return BeautifulSoup(response.text,type)


def initEPO(consumer_key = 'a66G2Ox2G6JYLlp9VTQnZ6Dqb7GGtmdn',
                consumer_secret_key='6EAoLMWT7gHZBGqy'):
    return epo_ops.Client(key=consumer_key, secret=consumer_secret_key)


def allEPO(where="ta", list=[]):
    ##Criterio de busqueda, todos los documentos que contengas todas las palabras de list en where
    ## ej. where="ta" list=["green", "energy"] busca todos los documentos que contengas green energy en sus titulos o abstract.
    aux = where+' all  "'
    for i in range(len(list)):
        if i == 0:
            aux += list[i]
        elif i>=5:
            aux +=', '+list[i]
            break
        else:
            aux += ', '+list[i]
    return aux+'"'


def anyEPO(where="ta", list=[]):
    #Criterio de busqueda, todos los documentos que contengas alguna de las palabras de list en where
    ## ej. where="ta" list=["green", "energy"] busca todos los documentos que contengas green o energy en sus titulos o abstract.
    ## maximo de 5 palabras.
    aux = where+' any  "'
    for i in range(len(list)):
        if i == 0:
            aux += list[i]
        elif i>=5:
            aux += ', '+list[i]
            break
        else:
            aux += ', '+list[i]
    return aux+'"'


def dataEPO(where="pd",data1="20150101",data2="20170101"):
    #Criterio de busqueda, entrega documentos entre las fechas data1 y data2
    #formato fecha data = AAAAMMDD
    ## ej. data1=20150101 data2=20170610 busca documentos entre el 01-01-2015 y 10-06-2017.
    return where+' within "'+data1+' '+data2+'"'


def countryEPO(where='pn',country='WO'):
    # Criterio de busqueda de patentes de un pais en especifico
    return where + '='+country


def proxEPO(where='ta',word1='green',word2='energy',dist=2,order='false'):
    #Criterio de busqueda de palabras a distancia espeficiada
    return where+'='+word1+' prox/distance<='+str(dist)+'/ordered='+order+' '+where+'='+word2


def andEPO(text1,text2):
    #concatena dos criterios de busqueda con el conector logico AND
    return text1+' and '+text2


def orEPO(text1,text2):
    #concatena dos criterios de busqueda con el conector logico OR
    return text1+' or '+text2


def findJsonPn(response):
    country, number, kind = [],[],[]
    aux = getSoup(response)
    response_json = json.dumps(xmltodict.parse(str(aux)),indent=4, separators=(',', ': '))
    response_js = json.loads(response_json)
    obj = response_js['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['ops:publication-reference']
    #print(obj)

    for i in range(len(obj)):
        country.append(obj[i]['document-id']['country'])
        number.append(obj[i]['document-id']['doc-number'])
        kind.append(obj [i]['document-id']['kind'])
        #print(country[i]+number[i]+kind[i])
    return country,number,kind


def findJsonAb(response_js):
    obj = response_js['ops:world-patent-data']['exchange-documents']['exchange-document']
    #print(response_js)

    for i in range(len(obj)):
        abs = obj['abstract'][i]['p']
        lan = obj['abstract'][i]['@lang']
        if minimizar(lan)=='en':
            return abs
    return None


def findJsonIPC(response_js):
    obj = response_js['ops:world-patent-data']['exchange-documents']['exchange-document']['bibliographic-data']['patent-classifications']
    #print(response_js)

    ipc = []
    for i in range(len(obj)):
        section = obj['patent-classification'][i]['section']
        clase = obj['patent-classification'][i]['class']
        subclase = obj['patent-classification'][i]['subclass']
        maingroup = obj['patent-classification'][i]['main-group']
        subgroup = obj['patent-classification'][i]['subgroup']
        class_value = obj['patent-classification'][i]['classification-value']
        ipc.append(section+clase+subclase+maingroup+'/'+subgroup)
    return ipc


def findJsonApplicant(response_js):
    obj = response_js['ops:world-patent-data']['exchange-documents']['exchange-document']['bibliographic-data']['parties']['applicants']['applicant']
    #print(response_js)

    for i in range(len(obj)):
        app = obj[i]['applicant-name']['name']
        lan = obj[i]['@data-format']
        if minimizar(lan)=='epodoc':
            return app
    return None


def findJsonInventor(response_js):
    obj = response_js['ops:world-patent-data']['exchange-documents']['exchange-document']['bibliographic-data']['parties']['inventors']['inventor']
    #print(response_js)

    for i in range(len(obj)):
        app = obj[i]['inventor-name']['name']
        lan = obj[i]['@data-format']
        if minimizar(lan)=='epodoc':
            return app
    return None


def findJsonTitle(response_js):
    obj = response_js['ops:world-patent-data']['exchange-documents']['exchange-document']['bibliographic-data']['invention-title']
    #print(response_js)

    for i in range(len(obj)):
        try:
            title = obj[i]['#text']
            lan = obj[i]['@lang']
        except:
            pass
        if minimizar(lan)=='en':
            return title
    return None


def findJsonDate(response_js):
    obj = response_js['ops:world-patent-data']['exchange-documents']['exchange-document']['bibliographic-data']['publication-reference']['document-id']
    #print(response_js)
    dat = ''
    for i in range(len(obj)):
        dat = obj[i]['date']
    return dat


def numberResponse(response):
    aux = getSoup(response)
    response_json = json.dumps(xmltodict.parse(str(aux)),indent=4, separators=(',', ': '))
    response_js = json.loads(response_json)
    obj = response_js['ops:world-patent-data']['ops:biblio-search']['@total-result-count']
    return int(obj)



def Abstract(client, number, country, kind):
    response = abstract_helper(client, number, country, kind)
    abstract = busquedaLang(response, idioma='en', type='xml')
    return abstract


def abstract_helper(client, number, country, kind):
    response = client.published_data(reference_type='publication',
                                     input=epo_ops.models.Docdb(str(number), country, kind),
                                     constituents='abstract',
                                     )
    #print(getSoup(response).prettify())
    return response


def response_helper(client,cql,rbegin,rend):
    response = client.published_data_search(cql=cql,
                                            range_begin=rbegin,
                                            range_end=rend,
                                            constituents=None)
    return response


def findAllEPO(client, number, country, kind):
    ## Esta funcion retorna el abstract en ingles, la fecha, el codigo ipc, el solicitante y el inventor
    response = abstract_helper(client, number, country, kind)
    aux = getSoup(response)
    response_json = json.dumps(xmltodict.parse(str(aux)),indent=4, separators=(',', ': '))
    response_js = json.loads(response_json)
    try:
        ab = findJsonAb(response_js)
    except:
        ab = None

    try:
        dat = findJsonDate(response_js)
    except:
        dat = None

    try:
        ipc = findJsonIPC(response_js)
    except:
        ipc = None

    try:
        app = findJsonApplicant(response_js)
    except:
        app = None

    try:
        inv = findJsonInventor(response_js)
    except:
        inv = None

    return ab,dat,ipc,app,inv


## Funciones para generar codigo
def sentenceProcessing(text):
    c = text.split(';')
    lista = permuta(c)
    print(len(lista))
    sen_fin = []
    for sentences in lista:
        #print(sentences)
        aux = ' '.join(sentences[1:])
        aux2 = [sentences[0]] + [aux]
        sen_aux = []
        for sentence in aux2:
            aux = minimizar(str(sentence))
            aux = deletePunt(text=aux)
            aux = deleteStop(text=aux, leng='english')
            aux = stemmingLemmatizer(aux)
            sen_aux.append(aux)
        sen_fin.append(sen_aux)
    print(sen_fin)
    return sen_fin


def getCode(where, sen_fin, pn):
    cqls = []
    for senEn in sen_fin:
        if pn!=None:
            cql1 = countryEPO(country=pn)
            cql2 = ''
        for i in range(len(senEn)):
            if i == 0:
                aux = allEPO(where,senEn[i])
                if pn==None:
                    cql1 = aux
                else:
                    cql1 = andEPO(cql1,aux)
            elif i == 1:
                cql2 = anyEPO(where,senEn[i])
            else:
                aux = anyEPO(where,senEn[i])
                cql2 = andEPO(cql2,aux)
        if len(senEn)>1:
            cqls.append(cql1+' and '+cql2)
        else:
            cqls.append(cql1)
    return cqls