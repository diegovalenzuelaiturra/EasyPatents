import sqlite3
from text_processing import *


def createDBfts():
    conn = sqlite3.connect('../Database/ipc_database.db')
    conn.execute(
        "CREATE VIRTUAL TABLE ipc_database USING fts4(index, ipc_class, keywords, tokenize=porter)")
    conn.close()
    print('la tabla fue creada con exito')


def addDB(index, ipc_class, keywords):
    conn = sqlite3.connect('../Database/ipc_database.db')
    conn.execute('''INSERT INTO ipc_database VALUES (?,?,?)''', (index, ipc_class, keywords))
    conn.commit()
    conn.close()


def buildDB(path_os, path_list):
    list_file = open(path_list, 'r')
    index = 0
    for line in list_file:
        path_ipc_file = path_os + line.replace('\n', '')
        file_ipc = open(path_ipc_file, 'r')
        for line in file_ipc:
            [ipc_class, description] = line.split(';',1)
            ipc_class = str(ipc_class).replace(' ','')
            keywords = des2key(description)
            addDB(index, ipc_class, keywords)
            index += 1


def des2key(description):
    sentences = description.split()
    words = []
    for sentence in sentences:
        aux = minimizar(sentence)
        aux = delete_puntuation(text=aux)
        aux = deleteStop(text=aux)
        aux = stemmingLemmatizer(aux)
        for i in aux:
            if i not in words:
                words.append(i)
    return words


def main():
    createDBfts()
    path_os = '../ipc-aux/'
    path_list = path_os + 'ipc_list.txt'
    buildDB(path_os, path_list)


if __name__ == "__main__":
    main()