import re
import codecs

from urllib import request

def spam(adresse,nb_mails):

    url_visited = []
    url_tovisit = [adresse]
    emails_found = []
    
    for j in url_tovisit:
        if (len(emails_found)>nb_mails):
            break
        print('URL en cours :',j)
        print('Emails trouvés :',len(emails_found))
        try:
            if j not in url_visited:
                response = request.urlopen(j)
                
                rep = response.read()
                rep = rep.decode('ISO-8859-1')
                
                re_emails = re.compile('[a-zA-Z]+@[a-zA-Z]+\.[a-zA-Z]+')        
                re_url = re.compile('(http[s]?:\/\/([a-zA-Z\/]+|\.)+)')
                
                emails = re.findall(re_emails,rep)
                urls = re.findall(re_url,rep)
                
                for i in emails:
                    emails_found.append(i)

                for i in urls:
                    if i[0] not in url_tovisit:
                        url_tovisit.append(i[0])
        except:
            print('-------Erreur avec 1 URL invalide-------')
            pass
        url_visited.append(j)
        url_tovisit.remove(j)
    print('Emails :',emails_found)


if __name__ == '__main__':
    #http://www.gutenberg.org/fifles.2554/2554.txt
    #deuxieme paramètre : nombre d'emails souhaités
    spam('http://www.google.fr',4)
