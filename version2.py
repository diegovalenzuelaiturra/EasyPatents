## Librerias para operar con la base de datos
from text_processing import *
from search_db import *

## Librerias para operar con las respuestas de typeform
from linkTypeform import*
from datetime import datetime
import calendar
import time

## Librerias para crear los reportes
from Report import getReport


def main():

    ## Leemos las bases de datos
    table_name = 'patentes2'
    db_file = '../Database/patentes2.db'

    table_name_ipc = 'ipc_database'
    db_file_ipc = '../Database/ipc_database.db'

    try:
        db = database(table_name, db_file)
        db_ipc = database(table_name_ipc, db_file_ipc)
    except:
        print('error al abrir base de datos')
        return False


    ## Obtener resultados desde Typeform
    name_id, mail_id, word_id = 'textfield_CGua','email_SLgj','textarea_pOCT'
    text_id, title_id = 'textarea_f0ne','textfield_xIp1'

    ## Tomamos el tiempo para poder determinar despues cuantas respuestas no hemos procesado entre ciclos
    d = datetime.utcnow()
    timestamp1 = str(calendar.timegm(d.utctimetuple()))

    ## Generamos un contador de solicitudes pardiendo en N°30000000
    count = 30000000

    ## Buscaremos en texto en los abstract
    where = 'abstract'

    ## Iniciamos un ciclo
    while (True):
        ## Recibimos las solicitudes desde typeform
        d = datetime.utcnow()
        timestamp2 = str(calendar.timegm(d.utctimetuple()))

        if timestamp1 == '':
            content = getFormComplete(typeform_UID='Ea4LIG', until=timestamp1)
        else:
            content = getFormComplete(typeform_UID='Ea4LIG', since=timestamp1)
        timestamp1 = timestamp2

        nombre, mail, keywords, description, project = getResponses(content=content, id=name_id),\
                                  getResponses(content=content, id=mail_id), \
                                  getResponses(content=content, id=word_id),\
                                  getResponses(content=content, id=text_id), \
                                  getResponses(content=content, id=title_id)

        ## Respondemos a las solicitudes
        for request_id in range(len(nombre)):

            ## Limpiamos el texto de puntuacion y toquenizamos
            words = getWords(keywords[request_id])

            ## Buscamos en nuestra base de datos las palabras solicitadas para generar los IPC
            get_ipc = generateIPC(table_name_ipc, db_ipc, words)
            topkipc = topK_IPC(get_ipc, 5)
            print(topkipc)

            ## Buscamos en nuestra base de datos con los IPC generados
            responses = db.searchMULT('ipc',topkipc)
            makeCSV(count, responses, description[request_id])

            ## Generamos el informe a enviar
            getReport(str(count) + '_sort.csv', 'main', nombre[request_id], project[request_id], words,
                      'hasta el 31 de julio')

            ## Enviamos el correo
            correo(count, mail[request_id], keywords[request_id])
            count += 1

        print(" I'm awake motherfuckers!!!! lml ")
        time.sleep(60)


def test():
    ## Leemos las bases de datos
    table_name = 'patentes2'
    db_file = '../Database/patentes2.db'

    table_name_ipc = 'ipc_database'
    db_file_ipc = '../Database/ipc_database.db'

    try:
        db = database(table_name, db_file)
        db_ipc = database(table_name_ipc, db_file_ipc)
    except:
        print('error al abrir base de datos')
        return False


    keywords = 'explosive plastic booster anfo robust'
    description = 'explosive plastic booster anfo robust'
    nombre = 'ribanez'
    project = 'plastic explosive'

    count = 1000
    ## Limpiamos el texto de puntuacion y toquenizamos
    words = getWords(keywords)

    ## Buscamos en nuestra base de datos las palabras solicitadas para generar los IPC
    get_ipc = generateIPC(table_name_ipc, db_ipc, words)
    topkipc = topK_IPC(get_ipc, 5)
    print(topkipc)

    ## Buscamos en nuestra base de datos con los IPC generados
    responses = db.searchMULT('ipc', topkipc)
    print(responses)
    if responses != None:
        makeCSV(count, responses, description)

        ## Generamos el informe a enviar
        getReport(str(count) + '_sort.csv', 'main', nombre, project, words,
                  'hasta el 31 de julio')
    else:
        print('respuesta vacia, nada que reportar')


if __name__ == "__main__":
    test()
    #main()