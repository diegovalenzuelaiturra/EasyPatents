from bs4 import BeautifulSoup

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
    #for i in aux:
    return aux.p.string


def publicNumber(country,number):
    aux = list()
    for i in range(len(country)):
        aux.append(str(country[i])+str(number[i]))
    return aux


def getSoup(response,type='html.parser'):
    return BeautifulSoup(response.text,type)

