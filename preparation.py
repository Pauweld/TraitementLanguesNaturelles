import re
import nltk
from nltk.stem.snowball import SnowballStemmer as ss
from nltk.stem.porter import *
from nltk.stem import LancasterStemmer
from nltk.stem import RegexpStemmer

def gutHeaders(txt, name):
    fichier = open(txt, 'r', encoding="utf-8")
    fin_head = 0
    # retire header
    while (fin_head != 24):
        fichier.readline()
        fin_head += 1
    body = ""
    # retire footer
    lines = fichier.readlines()
    for line in lines:
        if '*** END OF THIS PROJECT' in line:
            break
        body += line
        
    fichier2 = open('data/'+name+'0.txt', 'w')
    fichier3 = open('data/'+name+'1.txt', 'w')
    fichier4 = open('data/'+name+'2.txt', 'w')

    #première version
    p = re.compile('[a-zA-Z]+')
    words = re.findall(p, body)
    words2 = []
    for i in range(0,len(words)):
        if(words[i].isupper()):
            words[i] = words[i].lower()
            fichier2.write(words[i])
            fichier2.write('\n')
            words2.append(words[i])
        elif(words[i].islower()):
            fichier2.write(words[i])
            fichier2.write('\n')
            words2.append(words[i])

    #deuxieme version
    set_words = set(words2)
    for w in set_words:
        fichier3.write(w)
        fichier3.write('\n')

    #troisième version
    order_words = sorted(set_words)
    for w in order_words:
        fichier4.write(w)
        fichier4.write('\n')

    return order_words


def stemmer_snowball_en():
    fichier = open('data/en2_snowball.txt', 'w')
    fr2 = gutHeaders('data/texte-en.txt', 'en')
    fs = ss("english")
    for w in fr2:
        #print(w, "  ", fs.stem(w))
        #fichier.write(w)
        #fichier.write("  ")
        fichier.write(fs.stem(w))
        fichier.write("\n")

def stemmer_snowball_fr():
    fichier = open('data/en2_snowball.txt', 'w')
    fr2 = gutHeaders('data/texte-fr.txt', 'en')
    fs = ss("english")
    for w in fr2:
        #print(w, "  ", fs.stem(w))
        #fichier.write(w)
        #fichier.write("  ")
        fichier.write(fs.stem(w))
        fichier.write("\n")

def stemmer_porter_en():
    fichier = open('data/en2_porter.txt', 'w')
    en2 = gutHeaders('data/texte-en.txt', 'en')
    ps = PorterStemmer()
    for w in en2:
        #fichier.write(w)
        #fichier.write("  ")
        fichier.write(ps.stem(w))
        fichier.write("\n")

def stemmer_lancaster_en():
    fichier = open('data/en2_lancaster.txt', 'w')
    en2 = gutHeaders('data/texte-en.txt', 'en')
    ls = LancasterStemmer()
    for w in en2:
        fichier.write(ls.stem(w))
        fichier.write("\n")

def myRegexStemmer():
    en2 = gutHeaders('data/texte-en.txt', 'en')
    p = re.compile('ly|able|ing|ed|ion|er|ous$')
    st = RegexpStemmer(p, min=4)
    for w in en2:
        print(st.stem(w))

def comparStemmers():
    fichier = open('data/comparStemmers.txt', 'w')
    en2 = gutHeaders('data/texte-en.txt', 'en')
    ps = PorterStemmer()
    ls = LancasterStemmer()
    p = re.compile('ly|able|ing|ed|ion|er|ous$')
    st = RegexpStemmer(p, min=4)
    porter = []
    lancaster = []
    myStem = []
    for w in en2:
        fichier.write(w)
        fichier.write("\t")
        fichier.write(ps.stem(w))
        porter.append(ps.stem(w))
        fichier.write("\t")
        fichier.write(ls.stem(w))
        lancaster.append(ls.stem(w))
        fichier.write("\t")
        fichier.write(st.stem(w))
        myStem.append(st.stem(w))
        fichier.write("\n")
    print('-porter/lancaster-')
    print(len(set(porter))/len(set(lancaster)))
    print('-porter/myRegStemmer-')
    print(len(set(porter))/len(set(myStem)))
    print('-lancaster/myRegStemmer-')
    print(len(set(lancaster))/len(set(myStem)))
    

def getWordList():
    fichier = open('data/suffNwords.txt', 'w')
    en2 = gutHeaders('data/texte-en.txt', 'en')
    L = getSuffix()
    for cle in L:
        tmp = []
        fichier.write(cle[0][::-1])
        fichier.write("\t")
        fichier.write(cle[0])
        fichier.write("\t")
        for w in en2:
            if(cle[0][::-1] == w[:len(cle[0]):-1]):
                tmp.append(w)
        tmp = sorted(tmp)
        fichier.write(str(tmp))
        fichier.write("\n")

def getSuffix():
    en2 = gutHeaders('data/texte-fr.txt', 'fr')
    L = dict()
    i = 1
    while i <= 8:
        for w in en2:
            try:
                if w[-i:] in L:
                    L[w[-i:]] += 1
                else:
                    L[w[-i:]] = 1
            except:
                pass
        i += 1
    S = dict()
    for k in L:
        if L[k] > 20:
            S[k] = L[k]
    #print("suffixes=", sorted(S.items()), "\n")
    return sorted(S.items())

def testeSuffixe(suffix, nbMots, L):
    suffixesTrouves = []
    suffixesAtester = []
    suffixesAtester_tempo = []
    S_nbMots=80
    S_nbMinLettres=9
    S_nbOccLettre=0.4
    S_nbOccLettreGroupe=0.3
    S_Groupe = 0.7
    N = len(L)
    S_nbOccLettre2 = int(S_nbOccLettre * float(nbMots))
    S_nbOccLettre2Groupe = int(S_nbOccLettreGroupe * float(nbMots))
    S_Groupe2 = int(S_Groupe * float(nbMots))
    somme = 0
    if nbMots < S_nbMots:
        return None
    else:
        for l in L:
            newSuffix = l[0]
            if l[1] > S_nbOccLettre2:
                suffixesAtester.append(newSuffix)
                print('l[1]=',l[1], ', S_nbOccLettre2=',S_nbOccLettre2)
                print('on continue l\'évaluation avec [', newSuffix, ']') 
            elif l[1] > S_nbOccLettre2Groupe:
                suffixesAtester_tempo.append(newSuffix)
                somme=somme+l[1]
        if somme > S_Groupe2:
            for s in suffixesAtester_tempo:
                if s not in suffixesAtester:
                    suffixesAtester.append(s)
        if len(suffixesAtester)==0:
            if N > S_nbMinLettres:
                suffixesTrouves.append(True)
                print('N=', N, ', S_nbMinLettres=', S_nbMinLettres)
                print('[', suffix, '] est un suffixe')
        return suffixesAtester

def getProtoSuffixes():
    fichier = open('data/suffProto.txt', 'w')
    L = getSuffix()
    L_in = dict()
    suffProto = []
    suffixesAtester = []
    for i in L:
        if (len(suffixesAtester) != 0):
            while len(suffixesAtester) != 0:
                s = suffixesAtester[0]
                length = len(s)
                for j in L:
                    if(s in j[0][-length:] and len(j[0]) == length+1 and j[0] != s):
                        L_in[j[0]] = j[1]
                if (len(L_in) != 0):
                    L_in = sorted(L_in.items())
                    r = testeSuffixe(s, i[1], L_in)
                    L_in = dict()
                    if(r != None and len(r) > 0):
                        for k in r:
                            suffixesAtester.append(k)
                    else:
                    #if(r != None and isinstance(r, list) != True):
                        suffProto.append(s)
                suffixesAtester.pop(0)
        else:
            s = i[0]
            length = len(i[0])
            for j in L:
                if(s in j[0][-length:] and len(j[0]) == length+1 and j[0] != s):
                    L_in[j[0]] = j[1]
            if (len(L_in) != 0):
                L_in = sorted(L_in.items())
                r = testeSuffixe(s, i[1], L_in)
                L_in = dict()
                if(r != None and len(r) > 0):
                    for k in r:
                        suffixesAtester.append(k)
                else:
                #if(r != None and isinstance(r, list) != True):
                    suffProto.append(s)

    for suff in suffProto:
        fichier.write(suff)
        fichier.write("\n")
        
    return sorted(suffProto)
    
def getAllSuffixes():
    return ""

def DejeanStemmer():
    return ""
        
    

if __name__ == '__main__':
    #print(getSuffix())
    print(getProtoSuffixes())
