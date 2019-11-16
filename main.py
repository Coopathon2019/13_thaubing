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

