from EPmail import EPmail
from Busquedas import*
import epo_ops
from bs4 import BeautifulSoup


def main():

    apiurl = 'https://api.mailgun.net/v3/mail.easypatents.cl/messages'
    apikey = 'key-a4953915dffa936b1e83070c0de3c3ef'

    mtext = 'Hola! soy Ro, y te adjunto mi auxiliar 12'
    msubject = 'Auxiliar 12'
    mfrom = 'ribanez@easypatents.cl'
    mto = '@gmail.com'

    #archivos adjuntos
    fname = '/home/ribanez/Descargas/Auxiliar12.pdf'
    fformat = 'Auxiliar12.pdf'
    epm = EPmail(apiurl, apikey)
    #aux = epm.send_simple_message(mto, mfrom, msubject, mtext)
    #aux = epm.send_complex_message(mto,mfrom,msubject,mtext,fformat,fname)
    #print(aux)

    text = "son barcos de papel creados a partir de vibraciones de las hojas. Los barcos de papel tienen la resistencia del acero."
    #input('ingresa el texto, loco! ')
    #text = translateText('es','en', text)
    #text = deletePunt(text)
    #text = deleteStop('spanish', text)
    #text = deleteWord('PRP',text)
    #text = deleteWord('PRP$',text)
    #text = deleteWord('IN',text)
    #text = deleteWord('DT',text)

    #print(text)
    #text = stemmingLemmatizer(text)
    #print(text)
    #aux = collocationFinder(2,5,text)

    #word = "dog"
    #print(get_synonymous(word))
    #print(get_antonyms(word))

    #print(similaridad("dog","frump"))

    consumer_key = 'a66G2Ox2G6JYLlp9VTQnZ6Dqb7GGtmdn'
    consumer_secret_key = '6EAoLMWT7gHZBGqy'

    client = epo_ops.Client(key=consumer_key, secret=consumer_secret_key)  # Instantiate client

    response = client.published_data_search(cql='ab=explosive',range_begin=1,range_end=25,constituents=None)
    #
    # response = client.published_data(  # Retrieve bibliography data
    #     reference_type='publication',  # publication, application, priority
    #     input = epo_ops.models.Docdb('1000000', 'EP','A1'),  # original, docdb, epodoc
    #     #query='ti%3Dplastic' ,
    #     endpoint='biblio',  # optional, defaults to biblio in case of published_data
    #     constituents=[]  # optional, list of constituents
    # )

    #print(response.text)
    #print(soup.prettify())

    #count = 1
    #for aux in soup:
    #    print(aux)
    #    if count>3:
    #        break
    #    count+=1

    country = busquedaEPO(response,'country',type='html')
    number = busquedaEPO(response,'doc-number',type='html')
    kind = busquedaEPO(response, 'kind',type='html')
    #import epo_opsanonymous_client = epo_ops.Client()  # Instantiate a default client


    for i in range(len(country)):
        response = client.published_data(  # Retrieve bibliography data
            reference_type='publication',  # publication, application, priority
            input=epo_ops.models.Docdb(str(number[i]), country[i], kind[i]),  # original, docdb, epodoc
            endpoint='abstract',
            # optional, defaults to biblio in case of published_data
        )
        #aux = busquedaEPO(response,elemento='abstract',type='xml')
        #print(getSoup(response,'html.parser').find(lang='en').p.string)
        print(busquedaLang(response,idioma='en',type='html.parser'))
        #if len(aux)<=1:
        #    print(aux[0])
        #else:
        #    print(aux[1])



    #     text = response.text
    #     soup = BeautifulSoup(text, 'xml')
    #     aux2 = soup.find_all('abstract')
    #     #fin = list()
    #     for i in aux2:
    #         print(i.p.string)
        #print(response.text)
        #print(busquedaEPO(BeautifulSoup(response.text,'html.parser'),'abstract'))

if __name__ == "__main__":
    main()