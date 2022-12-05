from bs4 import BeautifulSoup
import requests

webpage = requests.get('https://www.cimri.com/oyuncak-bebekler')

sp = BeautifulSoup(webpage.content, 'html.parser')


#print(sp.text)

title = sp.find_all('a', 'title')

sellprice = sp.find_all('a', 's14oa9nh-0 lihtyI')
origprice = sp.find_all('a', 's14oa9nh-0 lihtyI')

titleLoop = [titles.text for titles in title]
sellPriceLoop = [sell.text for sell in sellprice]
origPriceLoop = [orig.text for orig in origprice]

print(titleLoop)