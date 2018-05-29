import sys
import nltk

nomeArqBase = sys.argv[1]
nomeArqConsulta = sys.argv[2]
print("Arquivo 1: " + sys.argv[1])
print("Arquivo 2: " + sys.argv[2])

#Identifica as stopwords
stopwords = nltk.corpus.stopwords.words("portuguese")
stemmer = nltk.stem.RSLPStemmer()

#Identifica os documentos
arqB = open(nomeArqBase, "r")
bases = arqB.readlines()
arqB.close()

arqC = open(nomeArqConsulta, "r")
consulta = arqC.readlines()
arqC.close()


#Número de arquivos dentro do base.txt
numArquivos = len(bases)

listaDicionarios = []
dictIndice = {}
def quebraPalavras(conteudoArquivo):
    palavrasArquivo = (nltk.word_tokenize(conteudoArquivo))
    return palavrasArquivo

def principal():
    contAux = 0

    #For para ler o conteúdo de cada arquivo dentro do base.txt
    for i in range(0,numArquivos):
        nomeArquivo = 'Bases/' + bases[i].replace('\n','')
        dictArquivo = {}                                                                        #Cria um dicionário para cada arquivo
        base = open(nomeArquivo, "r")                                                           #Abre arquivo
        conteudoArquivo = base.read()                                                           #Recebe o conteúdo de cada arquivo
        base.close()                                                                            #Fecha arquivo

        #Retira todos os caracteres( espaço em branco ( ), ponto (.), vírgula (,), exclamação (!), interrogação (?) e enter (\n))
        conteudoArquivo = (((conteudoArquivo.replace(',','')).replace('.','')).replace("!","")).replace("?",'')
        palavrasArquivo = quebraPalavras(conteudoArquivo)                                       #Separa todas as palavras do conteudo do arquivo.
        for j in palavrasArquivo:                                                               #Remove as stopwords do arquivo
            palavrasArquivo[contAux] = palavrasArquivo[contAux].lower()
            if j in stopwords:
                palavrasArquivo.remove(j)
            palavrasArquivo[contAux] = stemmer.stem(palavrasArquivo[contAux])                   #Substitui a palavra pelo seu radical
            if dictArquivo.get(palavrasArquivo[contAux]) == None:
                dictArquivo[palavrasArquivo[contAux]] = 1;
            else:
                dictArquivo[palavrasArquivo[contAux]] += 1;
            contAux += 1

        listaDicionarios.insert(len(listaDicionarios)+1,dictArquivo)
        contAux = 0

listaIndices2 = []                                                                              #Receberá o dicionário de cada arquivo
dict = {}                                                                                       #É o dicionário com todas as palavras, já com a contagem em todos arquivos


#for para percorrer a lista de dicionários de cada arquivo
def criaListaIndices():
    listaIndices = []

    for i in range(0, len(listaDicionarios)):
        listaIndices.insert(i,list(listaDicionarios[i]))                                        #Recebe a lista das palavras chaves do dicionário
        for j in range(0,len(listaIndices[i])):                                                 #For para percorrer o dicionário de cada arquivo
            if listaDicionarios[i].get(listaIndices[i][j]) != None:
                tupla = (i+1, listaDicionarios[i].get(listaIndices[i][j]))
                if dict.get(listaIndices[i][j]) == None:
                    dict[listaIndices[i][j]] = tupla
                else:
                    dict[listaIndices[i][j]] += tupla

    listaIndices = sorted(list(dict))
    indices = open('indices.txt', 'w')                                                          #Cria o arquivo indice.txt

    for i in range(0, len(listaIndices)):
        indices.write(listaIndices[i] + ': ')
        indices.write(str(dict.get(listaIndices[i])) + '\n')

    indices.close()


def buscaPalavra(palavra):                                                                      #Função retorna uma lista de arquivos de uma determinada palavra
    listaArquivos = []
    for i in range(0, len(listaDicionarios)):
        #print(listaDicionarios[i])
        if palavra in listaDicionarios[i].keys():
            listaArquivos.append(i)

    return listaArquivos

def intercessao(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]                                   #Faz a intercessao entre duas listas
    return lst3

def subLista(lst1,lst2):
    lst3 = [value for value in lst1 if value not in lst2]                               #Faz a subtracao entre duas listas
    return lst3

def uniao(lst):
    lstaux = []
    for i in lst:                                                                       #Faz a uniao entre duas listas
        for j in i:
            if j not in lstaux:
                lstaux.append(j)

    return lstaux


def realizaConsulta(consultaaux):
    consulta = consultaaux.split('|')
    aux = []

    lista = []
    listaAux = []
    for i in range(0,len(bases)):
        lista.append(i)


    for i in consulta:
        aux.append(i.replace(' ', '').split('&'))                               #Quebra a consulta no (OU), criando subconsultas de operadores AND(&)
    for i in aux:                                                               #Pega cada subconsulta
        listaR = lista                                                          #listaR recebe uma lista com a numeração dos arquivos bases
        for j in i:                                                             #Percorre cada palavra da lista de subconsulta
            if j[0] != '!':
                listaR = intercessao(listaR,buscaPalavra(stemmer.stem(j)))      #Se o primeiro caracter da palavra não for uma exclamação, busca os arquivos que a possui
                                                                                #e faz uma intercessão com a listaR
            else:
                auxL = buscaPalavra(stemmer.stem(j[1:]))
                listaR = intercessao(listaR,subLista(lista,auxL))               #Se for exclamação, pega todos os arquivos que não possui a palavra e faz a intercessão

        listaAux.append(listaR)


    return sorted(uniao(listaAux))                                              #Pega as lista de arquivos de cada subconsulta e faz a união


def geraResposta(consulta):                                                     #Função que gera o arquivo resposta.
    resposta = open('resposta.txt', 'w')  # Cria o arquivo resposta.txt
    lista = realizaConsulta(consulta)
    resposta.write(str(len(lista)) + '\n')
    print("Número de arquivos que correspondem a consulta: " + str(len(lista)))
    for i in lista:
        resposta.write(bases[i])
        print("Arquivo: " + bases[i].replace('\n',''))
    resposta.close()


def main():
    principal()
    criaListaIndices()
    print("Consulta: " + consulta[0])
    geraResposta(consulta[0])


if __name__ == '__main__':
    main()

