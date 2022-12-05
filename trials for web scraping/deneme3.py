from email.mime import image
import re
import requests
import os
from bs4 import BeautifulSoup

url = 'https://www.cimri.com/oyuncak-bebekler'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

images = soup.find_all('img')

#print(images)

for image in images:
    name = image['alt']
    link = image['src']
    print(name, link)