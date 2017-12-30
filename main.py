from EPmail import EPmail
from Scores import*
from BusquedasEPO import*
from linkTypeform import*
from datetime import datetime
import calendar
import time
import pandas as pd
from Report import getReport


def main():

    
    typeform_UID = ''
    
    
    ###Obtener resultados desde Typeform
    name_id, mail_id, word_id = 'textfield_CGua','email_SLgj','textarea_pOCT'
    text_id, title_id = 'textarea_f0ne','textfield_xIp1'
    pn = 'wo'

    d = datetime.utcnow()
    timestamp1 = str(calendar.timegm(d.utctimetuple()))
    count = 500
    while (True):
        ## Recibir respuestas de la pagina
        d = datetime.utcnow()
        timestamp2 = str(calendar.timegm(d.utctimetuple()))
        if timestamp1 == '':
            content = getFormComplete(typeform_UID=typeform_UID, until=timestamp1)
        else:
            content = getFormComplete(typeform_UID=typeform_UID, since=timestamp1)
        #print(content)
        timestamp1 = timestamp2

        nombre, mail, respuesta, text, project = getResponses(content=content, id=name_id),\
                                  getResponses(content=content, id=mail_id), \
                                  getResponses(content=content, id=word_id),\
                                  getResponses(content=content, id=text_id), \
                                  getResponses(content=content, id=title_id)

        ## Responder a las solicitudes
        where = 'ab' #donde se buscara en los documentos ab=abstract
        for k in range(len(respuesta)):
            words = getWordsText(respuesta[k])
            cql = getCode2(where, respuesta[k], pn)
            print(cql)
            searchResponse(count, cql, words, nombre[k],respuesta[k], text[k], project[k])
            correo(count,mail[k],respuesta[k])
            count+=1
        print('sleep')
        time.sleep(60)


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


def searchResponse(id,cql, words, nombre,respuesta,description,project):
    path = './Resultados/client'+str(id)
    #createCSV(path)
    a = 24#solicito 50 patentes por cql en batches de 25
    Abs_fin, Pns_fin, App_fin, Dat_fin, Ipc_fin, Inv_fin, Tit_fin = [], [], [], [], [], [], []
    #try:
    for k in range(a):
        client = initEPO()
        rbegin = (k)*40+1
        rend = (k+1)*40
        #try:
        response1 = response_helper(client,cql,rbegin,rend)
        #except:
        #    continue
        country,number,kind = findJsonPn(response1)
        final = numberResponse(response1)
        Abs,Pns,App,Dat,Ipc,Inv,Tit = [],[],[],[],[],[],[]
        for i in range(len(country)):
            ab, dat, ipc, app, inv, tit = findAllEPO(client,number[i],country[i],kind[i])
            #print(ab) #eliminar despues del debuggin
            pn = country[i] + number[i] + kind[i]
            if ab != None:
                Abs.append(ab),Dat.append(dat),Ipc.append(ipc),App.append(app)
                Inv.append(inv),Pns.append(pn),Tit.append(tit)
        Abs_fin += Abs
        Pns_fin += Pns
        App_fin += App
        Dat_fin += Dat
        Ipc_fin += Ipc
        Inv_fin += Inv
        Tit_fin += Tit

        if rend>=final:
            break
    makeCSV(Abs_fin, Pns_fin, App_fin, Dat_fin, Ipc_fin, Inv_fin, Tit_fin, description, words, path)
    getReport(path + '-sort.csv', 'main', nombre, project, getWordsText(respuesta),
                  'hasta el 21 de julio')
    # except:
    #     "Error busqueda EPO"


def makeCSV(Abs_fin, Pns_fin, App_fin, Dat_fin, Ipc_fin, Inv_fin, Tit_fin, description, words, path):
        pca_score = ScoreTextToAbstract(description, Abs_fin, words, Tit_fin)
        df_pca_score = pd.DataFrame(pca_score, columns=['PCA Score'])
        df_pn = pd.DataFrame(Pns_fin,columns=['Pn'])
        df_tit = pd.DataFrame(Tit_fin, columns=['Title'])
        df_abs = pd.DataFrame(Abs_fin, columns=['Abstract'])
        df_dat = pd.DataFrame(Dat_fin, columns=['Date'])
        df_app = pd.DataFrame(App_fin, columns=['Applicant'])
        df_ipc = pd.DataFrame(Ipc_fin, columns=['IPC'])
        df_inv = pd.DataFrame(Inv_fin, columns=['Inventor'])
        df_pca_abstracts = pd.concat([df_pca_score,df_pn,df_tit, df_abs,df_dat,df_app,df_inv,df_ipc], axis=1)
        df = df_pca_abstracts.sort_values(['PCA Score'], ascending=False)
        df.drop_duplicates(subset=['Pn'], inplace=True)
        df.to_csv(path+'-sort.csv')
        try:
            aux = len(df_abs)
            if aux>20:
                mutualScoreAbs(df_abs[:20], path)
            else:
                mutualScoreAbs(df_abs, path)
        except:
            print("error mutual Score Abstract")
        #writeCSV(data, pca_score, Pns, abstracts)
        #sortCSV(data+'-sort.csv',data+'.csv')


def correo(id,mail,respuesta):
    itext = "Estimad@, \n respondo a lo que solicito usando las palabras ["
    ftext = """\n Cualquier duda por favor contacta a patents@easypatents.cl \n Saludos Cordiales"""

    msubject = 'Vigilancia Tecnologica EasyPatents'
    mfrom = 'ro-bot@easypatents.cl'

    epm = EPmail()
    fname = './Report/main.pdf'
    fformat = './' + 'client'+str(id)+ '-report.pdf'
    mmessage = itext + respuesta + ' ] ' + ftext
    aux = epm.send_complex_message(mail,mfrom,msubject,mmessage,fformat,fname)
    print(aux)


if __name__ == "__main__":
    main()
    # client = initEPO()
    # rbegin = 1
    # rend = 41
    # cql = 'ipc any  "A02 , B01 , C01 , D01 , E01 , H32"'
    # response1 = response_helper(client, cql, rbegin, rend)
    # print(response1)
