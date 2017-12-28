# -*- coding: utf-8 -*-

import http.client
import re

sahibindenUrl = "www.sahibinden.com"
noticeAdditional = "/ilan/hayvanlar-alemi-buyukbas-hayvanlar-"

noticeAdd1 = "/hayvanlar-alemi-buyukbas-hayvanlar?"
noticeAdd2 = "pagingOffset="
noticeAdd3 = "?date=1day&"
noticeAdd4 = "pagingSize=50&price_min=400&a7335=97086&a7335=97087&a7335=97088&a7335=97089&a7335=97082&a7335=97083&a7335=97084&a7335=97085&a7335=97090&a7335=97080&a7335=97091&a7335=97081&a7335=97092"

currentOffset = 50
count = 0

def connection(requestUrl):
    conn = http.client.HTTPSConnection(sahibindenUrl)
    conn.request("GET", requestUrl)
    response = conn.getresponse()
    data = response.read()
    htmlFile = str(data, 'utf-8')
    return htmlFile

def writeNamePhone(nameList, phoneList):
    if len(phoneList) > 1:
        with open("Günlük Büyükbaş Satanlar Listesi.txt", "a") as contactList:
                contactList.write(nameList[0] + ", " + phoneList[0] + ", " + phoneList[1] + "\r")

    else:
        with open("Günlük Büyükbaş Satanlar Listesi.txt", "a") as contactList:
                contactList.write(nameList[0] + ", " + ''.join(phone) + "\r")

noticeLinks = re.findall('<a href="/ilan/hayvanlar-alemi-buyukbas-hayvanlar-(.*?)">', connection(noticeAdd1 + noticeAdd3 + noticeAdd4))

for i in range(3):
    noticeLinks.extend(re.findall('<a href="/ilan/hayvanlar-alemi-buyukbas-hayvanlar-(.*?)">', 
                                connection(noticeAdd1 + noticeAdd3 + noticeAdd2 + str(currentOffset) + "&" + noticeAdd4)))
    currentOffset += 50
    print(str(currentOffset) + " adet link tarandı.")

for i in range(len(noticeLinks)):
    linkPageHtml = connection(noticeAdditional + noticeLinks[i])
    name = re.findall('<div class="username-info-area">\n                <h5>(.*?)</h5>', linkPageHtml)
    phone = re.findall('<span class="pretty-phone-part">(.*?)</span>', linkPageHtml)

    if not name:
        name = re.findall('class="user-profile-photo" height="50" width="50" alt="">\n                <h5>(.*?)</h5>', linkPageHtml)
        writeNamePhone(name, phone)

        count += 1
        print(str(count) + ". kişi eklendi.")

    else:
        writeNamePhone(name, phone)
            
        count += 1
        print(str(count) + ". kişi eklendi.")
    
print(str(count) + " adet kişi ile listeleme işlemi tamamlandı.")
