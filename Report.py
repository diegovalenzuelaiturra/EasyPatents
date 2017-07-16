from datetime import timedelta
from datetime import datetime
import csv
import re
import subprocess
import os


def createFile(name):
    file = open(name,'w')
    file.close()


def appendFile(name):
    file = open(name,'a')
    return file


def variableTex(comand,variable):
    aux = '\\'+'newcommand{'+'\\'+str(comand)+'}{'+str(variable).upper()+'}\n'
    return aux


def fileVariables(cliente,producto,keywords,periodo):
    file = './Report/variables.tex'
    createFile(file)
    f = appendFile(file)
    f.write(variableTex('Cliente',cliente))
    f.write(variableTex('Producto',producto))
    f.write(variableTex('Keywords',keywords))
    f.write(variableTex('Periodo',periodo))
    f.close()


def chapterResp(f_append):
    aux = '\\'+'''chapter{Resultados}\n A continuación se mostrarán los 10 resultados más 
    relevantes de la búsqueda, en caso de existir, el resto de los resultados pueden ser vistos en anexos.\n '''
    f_append.write(aux)

def addResp(f_append, pn, title, abs, date, words,i):
    dat = datetime.strptime(date,'%Y%M%d')
    year = timedelta(days=365)
    op_dat = dat + 2.5*year

    url = '\\href{'+linkEPO(pn)+'}{\\textcolor{blue}{'+pn+'}}'

    aux_pn = '\n'+' \\vspace{1cm}'+str(i+1)+'- \\textbf{Número de publicación:} '+ url + '\\\\ \n'
    f_append.write(aux_pn)
    aux_title = '\\' + 'textbf{Titulo:} ' + title + '\\\\ \n \n'
    f_append.write(aux_title)
    aux_date = '\\'+'textbf{Fecha de publicación:} '+ dat.strftime('%d de %b de %Y') + '\\\\ \n'
    f_append.write(aux_date)
    aux_op = '\\'+'textbf{Fecha para ingreso a fases nacionales:} '+ op_dat.strftime('%d de %b de %Y') + '\\\\ \n'
    f_append.write(aux_op)
    aux = clearAbs(abs)
    aux = destacarAbs(aux,words)
    aux_abs = '\\'+'textbf{Abstract:} '+aux+'\\\\ \n \n'
    f_append.write(aux_abs)


def destacarAbs(abs,words):
    aux = abs.lower()
    res = '\\colorbox{yellow}{'
    for word in words:
        if word in abs.lower():
            #big_regex = re.compile()
            aux2 = res+word+'}'
            aux = aux.replace(word,aux2)
    return aux


def TOPResultados(csv_file, words):
    file = './Report/resultados.tex'
    createFile(file)
    f = appendFile(file)
    chapterResp(f)
    ifile = open(csv_file, "r")
    read = csv.reader(ifile,delimiter=',')
    next(read, None)
    i = 0
    for row in read:
        if i>10:
            break
        addResp(f, row[2], row[3],row[4], row[5], words,i)
        i+=1
    f.close()


def linkEPO(pn):
    pn, data, kind = pn[0:2], pn[2:12], pn[12:14]
    url = "https://worldwide.espacenet.com/publicationDetails/biblio?DB=EPODOC&II=0&ND=3&adjacent=true&locale=en_EP&FT=D&date=20160331&CC=" \
          + pn + "&NR=" + data + kind + "&KC=" + kind + "#"
    return url


def compilerReport(namefile):
    #subprocess.call('ls', shell=True)
    os.chdir('./Report/')
    commands = [
        ['pdflatex', namefile + '.tex'],
        ['bibtex', namefile + '.aux'],
        ['pdflatex', namefile + '.tex'],
        ['pdflatex', namefile + '.tex']
    ]

    for c in commands:
        subprocess.call(c)
    os.chdir('..')


def getReport(csv_file,name_file,cliente,producto,keywords,periodo):
    #os.chdir('./Report/')
    fileVariables(cliente, producto, keywords, periodo)
    TOPResultados(csv_file, keywords)
    compilerReport(name_file)


def clearAbs(abstract):
    aux = re.sub(r'[^\x00-\x7f]',r' ',abstract)
    return aux

#a = "According to this invention there is provided an aqueous oxidizer solution containing a mixture of dissolved oxidizing salts, for use in the preparation of explosives formulations, which a crystallization point as low as below 0°C. The solution has a water content of 25% by mass or less and contains ammonium nitrate and calcium nitrate wherein the ratio of the the molar concentration of ammonium nitrate to calcium nitrate is preferably approximately 1. When the water content of the solution is 24% by mass or less, the solution further contains monomethylammonium nitrate. This solution can be used for manufacturing watergel explosives, or emulsion explosives or ANE's (ammonium nitrate emulsion suspension or gel explosives). It can be easily transported underground in deep level mines through relatively small diameter pipelines, using existing access ways and shafts, to the working places at which point it can then be converted into a watergel or emulsion explosive or an ANE."

#print(clearAbs(a))

#getReport('./Resultados/client500-sort.csv','main','enaex s.a.','explosivo px',['explosive','oil','water'],'1 de junio al 30 de junio')


