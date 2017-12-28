# -*- coding: utf-8 -*-

import http.client
import re

sahibindenUrl = "www.sahibinden.com"
noticeAdditional = "/ilan/hayvanlar-alemi-kucukbas-hayvanlar-"

noticeAdd1 = "/hayvanlar-alemi-kucukbas-hayvanlar?"
noticeAdd2 = "pagingSize=50" 
noticeAdd3 = "pagingOffset="
noticeAdd4 = "date=1day&a7336=97105&a7336=97106&a7336=97101&a7336=97102&a7336=97103&a7336=97104&a7336=97097&a7336=97098&a7336=97099&a7336=97100&a7336=97094&a7336=97095&a7336=97096&"

"pagingSize=50"
"pagingOffset=50&pagingSize=50"
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
        with open("Günlük Küçükbaş Satanlar Listesi.txt", "a") as contactList:
                contactList.write(nameList[0] + ", " + phoneList[0] + ", " + phoneList[1] + "\r")

    else:
        with open("Günlük Küçükbaş Satanlar Listesi.txt", "a") as contactList:
                contactList.write(nameList[0] + ", " + ''.join(phone) + "\r")

noticeLinks = re.findall('<a href="/ilan/hayvanlar-alemi-kucukbas-hayvanlar-(.*?)">', connection(noticeAdd1 + noticeAdd4 + noticeAdd2))

for i in range(10):
    noticeLinks.extend(re.findall('<a href="/ilan/hayvanlar-alemi-kucukbas-hayvanlar-(.*?)">', 
                                connection(noticeAdd1 + noticeAdd4 + noticeAdd3 + str(currentOffset) + "&" + noticeAdd2)))
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
