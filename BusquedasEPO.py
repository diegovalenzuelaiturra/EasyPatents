from bs4 import BeautifulSoup
import epo_ops


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