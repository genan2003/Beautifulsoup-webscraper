from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

cautare=input("Introduceti marca masinii pe care o doriti:")
marca=input("Introduceti modelul masinii pe care o doriti:")

ListaMasini = []
ListaPreturi = []
ListaLink = []

html_site = requests.get('https://www.autovit.ro/autoturisme/' + cautare + '/' + marca).text
soup = BeautifulSoup(html_site, 'lxml')
pages=soup.select("li.pagination-item span")
pages=list(dict.fromkeys(pages))
pages1=[elem.get_text() for elem in pages]
pages2=list(map(int,pages1))
# print(max(pages2))

for page in range(1,max(pages2)):
    html_site = requests.get('https://www.autovit.ro/autoturisme/'+cautare+'/'+marca+'?'+'page='+str(page)).text
    soup = BeautifulSoup(html_site, 'lxml')

    masina=soup.find('div',class_='ooa-ys55sm e19uumca13')
    masina1 = soup.findAll('div', class_='ooa-1nvnpye e1b25f6f5')
    pret=soup.findAll('span', class_='ooa-epvm6 e1b25f6f8')

    for x in masina1:
        text=x.find('a')
        ListaMasini.append(text.text.strip())

    for x in pret:
        text=x.text.strip()
        ListaPreturi.append(str(text).replace("b'",""))

    for link in soup.findAll('a'):
        if 'anunt' in str(link.get('href')):
            ListaLink.append(str(link.get('href')))

    ListaLink=list(dict.fromkeys(ListaLink))
    data = list(zip(ListaMasini, ListaPreturi, ListaLink))
    d = pd.DataFrame(data, columns=["Nume Masina", "Pret", "Link anunt"])
    d.to_excel("Masini.xlsx")


