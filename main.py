from EPmail import EPmail
from Scores import*
#from BusquedasSem import*
#from Codigos import*
from BusquedasEPO import*
from linkTypeform import*
from datetime import datetime
import calendar
import time
import pandas as pd

def main():
    ###Obtener resultados desde Typeform
    name_id, mail_id, text_id = 'textfield_D85lzVq29NwK','email_Zqrl80iApgim','textarea_BiFS9A3GtmUs'
    pn = 'WO'

    d = datetime.utcnow()
    timestamp1 = str(calendar.timegm(d.utctimetuple()))
    count = 500
    while (True):
        ## Recibir respuestas de la pagina
        d = datetime.utcnow()
        timestamp2 = str(calendar.timegm(d.utctimetuple()))
        if timestamp1 == '':
            content = getFormComplete(typeform_UID='ZD0bjr', until=timestamp1)
        else:
            content = getFormComplete(typeform_UID='ZD0bjr', since=timestamp1)

        timestamp1 = timestamp2

        nombre, mail, respuesta = getResponses(content=content, id=name_id),\
                                  getResponses(content=content, id=mail_id), \
                                  getResponses(content=content, id=text_id)

        ## Responder a las solicitudes
        where = 'ab' #donde se buscara en los documentos ab=abstract
        for k in range(len(respuesta)):
            words = getWordsText(respuesta[k])
            sent = sentenceProcessing(respuesta[k])
            cqls = getCode(where, sent, pn)
            print(cqls)
            searchResponse(count, cqls, words)
            #correo(count,mail[k],respuesta[k])
            count+=1
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


def searchResponse(id,cqls,words):
    path = 'client'+str(id)
    createCSV(path+'.csv')
    a = int(25/25.0)
    Abs_fin, Pns_fin, App_fin, Dat_fin, Ipc_fin, Inv_fin = [], [], [], [], [], []
    for cql in cqls:
        for k in range(a):
            client = initEPO()
            rbegin = (k)*25+1
            rend = (k+1)*25
            try:
                response1 = response_helper(client,cql,rbegin,rend)
            except:
                pass
            country,number,kind = findJsonPn(response1)
            final = numberResponse(response1)
            Abs,Pns,App,Dat,Ipc,Inv = [],[],[],[],[],[]
            for i in range(len(country)):
                ab, dat, ipc, app, inv = findAllEPO(client,number[i],country[i],kind[i])
                pn = country[i] + number[i] + kind[i]
                if ab != None:
                    Abs.append(ab)
                    Dat.append(dat)
                    Ipc.append(ipc)
                    App.append(app)
                    Inv.append(inv)
                    Pns.append(pn)
            Abs_fin += Abs
            Pns_fin += Pns
            App_fin += App
            Dat_fin += Dat
            Ipc_fin += Ipc
            Inv_fin += Inv

            if rend>=final:
                break
    makeCSV(Abs_fin, Pns_fin, App_fin, Dat_fin, Ipc_fin, Inv_fin,words,path)



def makeCSV(Abs_fin, Pns_fin, App_fin, Dat_fin, Ipc_fin, Inv_fin,words,path):
        X = thoughtobeat(words, Abs_fin)
        pca_score = PCAscore2(X)
        df_pn = pd.DataFrame(Pns_fin,columns=['Pn'])
        df_pca_score = pd.DataFrame(pca_score, columns=['PCA Score'])
        df_abs = pd.DataFrame(Abs_fin, columns=['Abstract'])
        df_dat = pd.DataFrame(Dat_fin, columns=['Date'])
        df_app = pd.DataFrame(App_fin, columns=['Applicant'])
        #df_ipc = pd.DataFrame(Ipc_fin, columns=['IPC'])
        df_inv = pd.DataFrame(Inv_fin, columns=['Inventor'])
        df_pca_abstracts = pd.concat([df_pca_score,df_pn,df_abs,df_dat,df_app,df_inv], axis=1)
        df = df_pca_abstracts.sort_values(['PCA Score'], ascending=False)
        df.drop_duplicates(subset=['Pn'], inplace=True)
        df.to_csv(path+'-sort.csv')
        #mutualScoreAbs(df_abs,path)
        #writeCSV(data, pca_score, Pns, abstracts)
        #sortCSV(data+'-sort.csv',data+'.csv')


def correo(id,mail,respuesta):
    itext = "Estimad@, \n respondo a lo que solicito usando las palabras ["
    ftext = """\n Cualquier duda por favor contacta a patents@easypatents.cl \n Saludos Cordiales"""

    msubject = 'Vigilancia Tecnologica EasyPatents'
    mfrom = 'ro-bot@easypatents.cl'

    epm = EPmail()
    fname = './' + 'client'+str(id)+ '-sort.csv'
    fformat = 'resp.csv'
    mmessage = itext + respuesta + ' ] ' + ftext
    aux = epm.send_complex_message(mail,mfrom,msubject,mmessage,fformat,fname)
    print(aux)

if __name__ == "__main__":
    main()
