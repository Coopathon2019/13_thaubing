#!/usr/bin/python
# -*- coding: UTF-8 -*-
from lxml import etree
from io import BytesIO
from bs4 import BeautifulSoup
import requests
import json
import sys
from pyzbar.pyzbar import decode
import numpy as np
import cv2


def web_request(url,data,flag):
    if flag == 'get':
        response = requests.get(url,params=data)
    elif flag == 'post':
        response = requests.post(url,data=data)
    else:
        print('Please check your flag')
        return -1

    xml_bytes = response.content
    f = BytesIO(xml_bytes)
    parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.parse(f,parser=parser)
    return tree

def barcodeReader(image, bgr):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)

    for decodedObject in barcodes:
        points = decodedObject.polygon

        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

    for bc in barcodes:
        cv2.putText(frame, bc.data.decode("utf-8") + " - " + bc.type, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,bgr, 2)

        return "Barcode:{}".format(bc.data.decode("utf-8"))


#barcode scan
bgr = (8, 70, 208)
cap = cv2.VideoCapture(0)
find_flag=1
while (find_flag):
    ret, frame = cap.read()
    barcode = barcodeReader(frame, bgr)
    print(barcode)
    if barcode != None:
        barcode_to_name = barcode.split(':', 1 )[1]
        find_flag = 0
    cv2.imshow('Barcode reader', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break



#search company's name
name = barcode_to_name
data= {
    'MCANNO': name
}
url = 'http://www.gs1tw.org/twct/web/codesearch_send.jsp'

tree = web_request(url,data,flag='post')
try:
    content = [t.text for t in tree.xpath("/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/p[1]")]
    company = str(content[0])
    company = company[21:]
    print(company)
except:
    print("您掃的條碼查無結果請重新掃描")

#search company's Tax ID
data = {
        'q':company
}
url='http://company.g0v.ronny.tw/index/search?'

tree = web_request(url,data,flag='get')
try:
    tax_id = tree.xpath("//td[2]/text()")[0]
    print(tax_id)
except:
    print("您所查詢的公司並無營利事業單位統一編號")

#search company's scandal
data = {
    'facility_name':'',
    'corp_id':tax_id,
    'industry_name':'All',
    'factory_fine':'1',
    'id_2':'All',
}
url = 'https://thaubing.gcaa.org.tw/corp/search?'

tree = web_request(url,data,flag='get')
try:
    print(tree.xpath('//*[@id="block-system-main"]/div/div/div[2]/div/h4/span/a/text()')[0])
    print("開罰紀錄： " + tree.xpath('//*[@id="block-system-main"]/div/div/div[2]/div/div/span/text()')[0])
    detail = 'https://thaubing.gcaa.org.tw' + tree.xpath('//*[@id="block-system-main"]/div/div/div[2]/div/h4/span/a/@href')[0]
    print("相關開罰連結： " + detail)
except:
    print("資料庫查無環境違規紀錄")

#get google search result
google_url = 'https://www.google.com.tw/search'
my_params = {'q': company+' 污染'}

r = requests.get(google_url, params = my_params)

if r.status_code == requests.codes.ok:
  soup = BeautifulSoup(r.text, 'html.parser')


  items = soup.select('a[href^="/url"]')
  for i in items:
    print("搜尋結果: "  + i.text)
    print("連結: " + i.get('href'))
