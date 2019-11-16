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

