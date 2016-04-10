import requests
from bs4 import BeautifulSoup
import json

def req_sample():
    url = "http://data.bootex.xyz:8000/json"

    req = requests.get(url)
    return req.json()


def req_melon():
    url = "http://www.melon.com/album/detail.htm?albumId=2676884"

    req = requests.get(url)
    return BeautifulSoup(req.text)



#soup = req_melon()
#print (soup.select_one("div.ellipsis"))

from selenium import webdriver

url = "http://www.melon.com/album/detail.htm?albumId=2676884"
PROXY = "127.0.0.1:8118" # IP:PORT or HOST:PORT
fb_profile = webdriver.FirefoxProfile
fb_profile
fb = webdriver.Firefox()
fb.get(url)
