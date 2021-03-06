from bs4 import BeautifulSoup
import requests
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["meteo"]

start = '1850'
end = '2021'

# PRÉCIPITATIONS MAX/JOUR
colPre = mydb["precipitation"]
urlPre = 'http://meteo-climat-bzh.dyndns.org/mete68-' + \
    start+'-'+end+'-21-tn-1-0-0.php'

responsePre = requests.get(urlPre)

if responsePre.ok:
    soup = BeautifulSoup(responsePre.text, 'lxml')
    tds = soup.find('table', {'class': 'table1'}).findAll('td')

    i = 1
    j = 0
    l = 0.0
    k = 14
    p = 0
    t = 1

    while t < 14:

        if p == 1:
            t = t+1

        if i == 1:
            i = 2
            try:
                print(float(tds[k].text), end=' ')
                x = colPre.insert_one(
                    {"annee": float(tds[k].text.strip()), "mois": [], "moy": 0.0})
                l = float(tds[k].text)
                if float(tds[k].text) == float(end):
                    p = 1
            except:
                print(0, end=' ')
                l = float(tds[k].text)
                if float(tds[k].text) == float(end):
                    p = 1
                x = colPre.insert_one(
                    {"annee": float(0), "mois": [], "moy": 0.0})

        elif i == 2:
            try:
                print(float(tds[k].text), end=' ')
                x = colPre.update_one(
                    {"annee": l}, {"$push": {"mois": float(tds[k].text.strip())}})
            except:
                print(0, end=' ')
                x = colPre.update_one(
                    {"annee": l}, {"$push": {"mois": float(0)}})

            j = j+1
            if j == 12:
                i = 3
                j = 0

        elif i == 3:
            i = 1
            try:
                print(float(tds[k].text))
                x = colPre.update_one(
                    {"annee": l}, {"$set": {"moy": float(tds[k].text.strip())}})
            except:
                print(0)
                x = colPre.update_one(
                    {"annee": l}, {"$set": {"moy": float(0)}})

        k = k+1

# PRÉCIPITATIONS MAX/JOUR
colTemp = mydb["temperature"]
urlTemp = 'http://meteo-climat-bzh.dyndns.org/mete68-' + \
    start+'-'+end+'-3-tn-1-0-0.php'

responseTemp = requests.get(urlTemp)

if responseTemp.ok:
    soup = BeautifulSoup(responseTemp.text, 'lxml')
    tds = soup.find('table', {'class': 'table1'}).findAll('td')

    i = 1
    j = 0
    l = 0.0
    k = 14
    p = 0
    t = 1

    while t < 14:

        if p == 1:
            t = t+1

        if i == 1:
            i = 2
            try:
                print(float(tds[k].text), end=' ')
                x = colTemp.insert_one(
                    {"annee": float(tds[k].text.strip()), "mois": [], "moy": 0.0})
                l = float(tds[k].text)
                if float(tds[k].text) == float(end):
                    p = 1
            except:
                print(0, end=' ')
                l = float(tds[k].text)
                if float(tds[k].text) == float(end):
                    p = 1
                x = colTemp.insert_one(
                    {"annee": float(0), "mois": [], "moy": 0.0})

        elif i == 2:
            try:
                print(float(tds[k].text), end=' ')
                x = colTemp.update_one(
                    {"annee": l}, {"$push": {"mois": float(tds[k].text.strip())}})
            except:
                print(0, end=' ')
                x = colTemp.update_one(
                    {"annee": l}, {"$push": {"mois": float(0)}})

            j = j+1
            if j == 12:
                i = 3
                j = 0

        elif i == 3:
            i = 1
            try:
                print(float(tds[k].text))
                x = colTemp.update_one(
                    {"annee": l}, {"$set": {"moy": float(tds[k].text.strip())}})
            except:
                print(0)
                x = colTemp.update_one(
                    {"annee": l}, {"$set": {"moy": float(0)}})

        k = k+1
