import sqlite3


class database():

    def __init__(self, table_name, db_file):
        self.table = table_name
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)


    def search(self, where, query):
        if where == 'abstract':
            return self.conn.execute("SELECT * FROM patentes2 WHERE abstract MATCH ?",(query,))
        elif where == 'title':
            return self.conn.execute("SELECT * FROM patentes2 WHERE title MATCH ?", (query,))
        elif where == 'ipc':
            return self.conn.execute("SELECT * FROM patentes2 WHERE ipc_class MATCH ?", (query,))
        else:
            return None


    def searchAND(self, where, words):
        query = '"'
        index = 0

        for word in words:
            query = query + ' AND ' + word if index != 0 else query + word
            index = index + 1

        return self.search(where,query+'"')


    def searchOR(self, where, words):
        query = '"'
        index = 0

        for word in words:
            query = query + ' OR ' + word if index != 0 else query + word
            index = index + 1

        return self.search(where, query+'"')


    def searchMULT(self, where, words):
        query = ' '.join(words)
        if where == 'abstract':
            return self.conn.execute("SELECT * FROM patentes2 WHERE abstract MATCH ?",(query,))
        elif where == 'title':
            return self.conn.execute("SELECT * FROM patentes2 WHERE title MATCH ?", (query,))
        elif where == 'ipc':
            return self.conn.execute("SELECT * FROM patentes2 WHERE ipc_class MATCH ?", (query,))
        else:
            return None

def db_test():

    table_name = 'patentes2'
    db_file = '../Database/patentes2.db'
    try:
        db = database(table_name, db_file)
    except:
        print('error al abrir base de datos')
        return False

    try:
        db.search('title',"'bacteria'")
    except:
        print('error al buscar en el titulo')

    try:
        db.search('abstract',"'explosive'")
    except:
        print('error al buscar en el abstract')

    try:
        db.search('ipc',"'A23L3'")
    except:
        print('Error al buscar en los ipc')

    words = ['explosive', 'plastic']

    try:
        for response in db.searchAND('abstract', words):
            print(response)
    except:
        print('Error con searchAND')

    try:
        for response in db.searchOR('abstract', words):
            print(response)
    except:
        print('Error con searchOR')

    try:
        for response in db.searchMULT('abstract',words):
            print(response)
    except:
        print('Error searchMULT')

    return True


if __name__ == "__main__":

   print('El test fue exitoso' if db_test() else 'Fallo el test')