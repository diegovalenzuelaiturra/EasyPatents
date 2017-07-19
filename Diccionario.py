from gensim import corpora,models
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from xlrd import open_workbook


def BuildDict(path_os,path_dict,path_list):
    list_file = open(path_list,'r')
    dictionary_exist = False

    for line in list_file:
        path_xls = path_os+line.replace('\n','')
        book = open_workbook(path_xls)
        sheet = book.sheet_by_index(0)
        for row_idx in range(sheet.nrows):
            if row_idx>0:
                if dictionary_exist == False:
                    text = str(sheet.cell(row_idx, 0).value) + ' ' + str(sheet.cell(row_idx, 3).value) + ' ' + str(
                        sheet.cell(row_idx, 4).value) + ' ' + str(sheet.cell(row_idx, 17).value) + ' ' + str(
                        sheet.cell(row_idx, 40).value)
                    aux = getWords(text)
                    dictionary = corpora.Dictionary([aux])
                    dictionary_exist = True
                else:
                    text = str(sheet.cell(row_idx, 0).value) + ' ' + str(sheet.cell(row_idx, 3).value) + ' ' + str(
                        sheet.cell(row_idx, 4).value) + ' ' + str(sheet.cell(row_idx, 17).value) + ' ' + str(
                        sheet.cell(row_idx, 40).value)
                    aux = getWords(text)
                    dictionary.add_documents([aux])

    #once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq <= 5]
    #dictionary.filter_tokens(once_ids)
    dictionary.compactify()
    dictionary.save(path_dict)
    #print(dictionary.keys())


def BuildCorpus(path_os,path_dict,path_corpus,path_list):
    list_file = open(path_list,'r')
    dictionary = corpora.Dictionary.load(path_dict)
    corpus = []

    for line in list_file:
        path_xls = path_os+line.replace('\n','')
        book = open_workbook(path_xls)
        sheet = book.sheet_by_index(0)
        for row_idx in range(sheet.nrows):
            if row_idx>0:
                text = str(sheet.cell(row_idx, 0).value) + ' ' + str(sheet.cell(row_idx, 3).value) + ' ' + str(
                    sheet.cell(row_idx, 4).value) + ' ' + str(sheet.cell(row_idx, 17).value) + ' ' + str(
                    sheet.cell(row_idx, 40).value)
                aux = getWords(text)
                corpus.append(dictionary.doc2bow(aux))

    corpora.MmCorpus.serialize(path_corpus, corpus)



def getWords(text):
    sentences = text.split()
    words = []
    for sentence in sentences:
        aux = minimizar(sentence)
        aux = deletePunt(text=aux)
        aux = deleteStop(text=aux)
        aux = stemmingLemmatizer(aux)
        for i in aux:
            if i not in words:
                words.append(i)
    return words


def minimizar(text):
    return text.lower()


def stemmingLemmatizer(text):
    ps = WordNetLemmatizer()
    aux1 = []
    for i in text:
        aux1.append(ps.lemmatize(i))
    return aux1



def deletePunt(text):
    return RegexpTokenizer(r'\w+').tokenize(text)


def deleteStop(text):
    stop = set(stopwords.words('english'))
    aux = text
    for i in aux:
        if i in stop:
            aux.remove(i)
        elif len(i)<=3:
            aux.remove(i)
    return aux

def test():
    path_dict = 'patent.txtdic'
    path_os = './test/'
    path_list = path_os+'list.txt'
    path_corpus = 'patent.mm'
    BuildDict(path_os, path_dict, path_list)
    BuildCorpus(path_os,path_dict,path_corpus,path_list)
    dictionary = corpora.Dictionary.load(path_dict)
    print(dictionary.token2id)
    corpus = corpora.MmCorpus(path_corpus)
    print(corpus)
    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=20)
    print(ldamodel.print_topics(num_topics=3, num_words=3))
    ldamodel.save('lda.model')

if __name__ == "__main__":
    test()