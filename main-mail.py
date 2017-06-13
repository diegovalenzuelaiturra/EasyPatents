from EPmail import EPmail
from Busquedas import*
import epo_ops

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

    word = "dog"
    print(get_synonymous(word))
    #print(get_antonyms(word))

    print(similaridad("dog","frump"))
    client = epo_ops.Client(key='abc', secret='xyz')  # Instantiate client
    response = client.published_data(  # Retrieve bibliography data
        reference_type='publication',  # publication, application, priority
        input=epo_ops.models.Docdb('1000000', 'EP', 'A1'),  # original, docdb, epodoc
        endpoint='biblio',  # optional, defaults to biblio in case of published_data
        constituents=[]  # optional, list of constituents
    )


if __name__ == "__main__":
    main()