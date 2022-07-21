from bs4 import BeautifulSoup
import requests
import csv

file_name = 'cimri11.csv'


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

source = requests.get('https://www.cimri.com/oyuncak-bebekler', headers = headers).text
soup = BeautifulSoup(source, 'lxml')

title = []
price1 = []
price2 = []


# for loop
innerContent = soup.find('div', class_="s1cegxbo-1 cACjAF")

li_items_names = innerContent.find_all('h3', {'class':'product-title'})
price_content = innerContent.find_all('a', {'class':'s14oa9nh-0 lihtyI'})



for i in li_items_names:
    string = i.text
    title.append( string.strip() )
    print(string.strip())

B = 0

for i in price_content:
    if(B == 0):
        string = i.text
        price1.append( string.strip() )
        print('B: ', B, 'PRICE 1:', string.strip())
        B += 1

    if(B == 1):
        for i in price_content:
            string = i.text
            price2.append( string.strip() )
            print('SECOND:', string.strip())
        B = 0

with open(file_name, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Sr.No', 'Name', 'Prices1', 'Prices2'])
    for i in range(len(title)):
        writer.writerow([i, title[i], price1[i], price2[i]])
