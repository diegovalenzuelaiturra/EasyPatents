import sqlite3


class database():

    def __init__(self, table_name, db_file):
        self.table = table_name
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)


    def search(self, where, query):

        if self.table == 'patentes2':
            if where == 'abstract':
                return self.conn.execute("SELECT * FROM patentes2 WHERE abstract MATCH ?", (query,))
            elif where == 'title':
                return self.conn.execute("SELECT * FROM patentes2 WHERE title MATCH ?", (query,))
            elif where == 'ipc':
                return self.conn.execute("SELECT * FROM patentes2 WHERE ipc_class MATCH ?", (query,))
            else:
                return None

        elif self.table == 'ipc_database':
            if where == 'keywords':
                return self.conn.execute("SELECT * FROM ipc_database WHERE keywords MATCH ?",(query,))
            elif where == 'ipc':
                return self.conn.execute("SELECT * FROM ipc_database WHERE ipc_class MATCH ?", (query,))
            else:
                return None


    def searchAND(self, where, words):
        query = '"'
        index = 0

        for word in words:
            query = query + ' AND ' + word if index != 0 else query + word
            index = index + 1

        return self.search(self.table, where,query+'"')


    def searchOR(self, where, words):
        query = '"'
        index = 0

        for word in words:
            query = query + ' OR ' + word if index != 0 else query + word
            index = index + 1

        return self.search(where, query+'"')


    def searchMULT(self, where, words):
        query = '"'+' '.join(words)+'"'
        if where == 'abstract':
            return self.conn.execute("SELECT * FROM patentes2 WHERE abstract MATCH ?",(query,))
        elif where == 'title':
            return self.conn.execute("SELECT * FROM patentes2 WHERE title MATCH ?", (query,))
        elif where == 'ipc':
            return self.conn.execute("SELECT * FROM patentes2 WHERE ipc_class MATCH ?", (query,))
        else:
            return None


def db_test():

    table_name_wipo = 'patentes2'
    db_file_wipo = '../Database/patentes_3.db'

    table_name_ipc = 'ipc_database'
    db_file_ipc = '../Database/ipc_database.db'


    try:
        db_wipo = database(table_name_wipo, db_file_wipo)
    except:
        print('error al abrir base de datos')
        return False

    try:
        responses = db_wipo.search('title',"'car'")
        print(responses.description)
    except:
        print('error al buscar en el titulo')

    try:
        db_wipo.search('abstract',"'explosive'")
    except:
        print('error al buscar en el abstract')

    try:
        db_wipo.search('ipc',"'A23L3'")
    except:
        print('Error al buscar en los ipc')

    words = ['explosive', 'plastic']

    try:
        for response in db_wipo.searchAND('abstract', words):
            print(response)
    except:
        print('Error con searchAND')

    try:
        for response in db_wipo.searchOR('abstract', words):
            print(response)
    except:
        print('Error con searchOR')

    topipc = ['F41A', 'F16B', 'E01C', 'E06B', 'B63B']

    #try:
    for ipc in topipc:
        responses = db_wipo.search('ipc', ipc)
        for response in responses:
            print(response)
    responses = db_wipo.searchMULT('ipc', topipc)
    #except:
    #    print('Error searchMULT')


    #return True


if __name__ == "__main__":

   print('El test fue exitoso' if db_test() else 'Fallo el test')