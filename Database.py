import sqlite3
from xlrd import open_workbook
import gensim
import numpy as np
import string

wiki400 = '../glove.6B/wiki.txt'
model = gensim.models.KeyedVectors.load_word2vec_format(wiki400, binary=False)


def makevector(palabras):
    v_usr = np.zeros(len(model['man']))
    for i in palabras:
        try:
            v_usr += model[i]
        except:
            pass
    if len(palabras) == 0:
        v_usr = (1 / 1e-8) * v_usr
    else:
        v_usr = (1 / len(palabras)) * v_usr
    return v_usr  # ,v_vec


def createDBfts():
    conn = sqlite3.connect('../Database/patentes2.db')
    conn.execute(
        "CREATE VIRTUAL TABLE patentes2 USING fts4(index, publication_number, publication_date, ipc_class, applicant, inventor, abstract, title, vector, tokenize=porter)")
    conn.close()
    print('la tabla fue creada con exito')


def addDB(index, publication_number, publication_date, ipc_class, applicant, inventor, abstract, title, vector):
    conn = sqlite3.connect('../Database/patentes2.db')
    conn.execute('''INSERT INTO patentes VALUES (?,?,?,?,?,?,?,?,?)''',
                 (index, publication_number, publication_date, ipc_class, applicant, inventor, abstract, title, vector))
    conn.commit()
    conn.close()


def addDBfts(index, publication_number, publication_date, ipc_class, applicant, inventor, abstract, title, vector):
    conn = sqlite3.connect('../Database/patentes2.db')
    conn.execute('INSERT INTO patentes2 VALUES (?,?,?,?,?,?,?,?,?)',
                 (index, publication_number, publication_date, ipc_class, applicant, inventor, abstract, title, vector))
    conn.commit()
    conn.close()


def buildDB(path_os, path_list):
    list_file = open(path_list, 'r')
    index = 0
    for line in list_file:
        path_xls = path_os + line.replace('\n', '')
        book = open_workbook(path_xls)
        sheet = book.sheet_by_index(0)
        for row_idx in range(sheet.nrows):
            if row_idx > 0:
                abstract = str(sheet.cell(row_idx, 65).value)
                kind = str(sheet.cell(row_idx, 2).value)
                if not kind == 'S' and not abstract == '-':
                    publication_number = str(sheet.cell(row_idx, 0).value)
                    publication_date = str(sheet.cell(row_idx, 10).value)
                    ipc_class = str(sheet.cell(row_idx, 62).value)  # podria ser el 62
                    applicant = str(sheet.cell(row_idx, 67).value)
                    inventor = str(sheet.cell(row_idx, 46).value)
                    title = str(sheet.cell(row_idx, 66).value)
                    palabras = abstract.split()
                    vector = makevector(palabras)  # vector del abstract !!!
                    vec_str = ';'.join(str(vec) for vec in vector)
                    # addDB(index, publication_number, publication_date, ipc_class, applicant, inventor, abstract, title, vec_str)
                    addDBfts(index, publication_number, publication_date, ipc_class, applicant, inventor, abstract,
                             title, vec_str)
                    index += 1


def main():
    createDBfts()
    path_os = '../UNZIP_WIPO/'
    path_list = path_os + 'wipo.txt'
    buildDB(path_os, path_list)


if __name__ == "__main__":
    main()