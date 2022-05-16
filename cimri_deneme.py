from bs4 import BeautifulSoup
import requests
import csv

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

source = requests.get('https://www.cimri.com/oyuncak-bebekler', headers = headers).text
soup = BeautifulSoup(source, 'lxml')

# print(soup.prettify())

Names = []
Prices1 = []
Prices2 = []

# for loop
innerContent = soup.find('div', class_="s1cegxbo-1 cACjAF")
priceContent = soup.find('div', class_="top-offers")

content = soup.find_all('div', class_="z7ntrt-0 cLlfW s1a29zcm-11 ggOMjb")
li_items_names = innerContent.find_all('h3', {'class':'product-title'})

price_content = innerContent.find_all('a', {'class':'s14oa9nh-0 lihtyI'})


for i in li_items_names:
    string = i.text
    Names.append( string.strip() )
    #Prices1.append( string.strip() )
    #Prices2.append( string.strip() )

for a in li_items_names:
    li_items_prices = soup.find_all('a', {'class':'s14oa9nh-0 lihtyI'})
    index = 0
    for i in li_items_prices:
        #print(i)
        #li = i.find('div', {'class':'tag'}) #site ismi çekiliyor!
        #print(li.text)
        #print(i.text)
        #price = i.get_text()
      
        if(index == 0):
            price = i.get_text()
            splitted_1 = price.split(".com")
            # s = splitted_1.[1]
            print(splitted_1[0])

            x1 = splitted_1[0].split(".tr")
            #splitted_2 = s.split("com")
            #print(x1)

            x2 = x1[0].split("TL")
            #splitted_2 = s.split("com")
            #print(x2)

            #Prices1.append(x2[0])
            #print(x2[0])
            Prices1.append(x2[0])
            index += 1
            
        if(index == 1):
            Prices2.append(i.get_text())
            index = 0

file_name = 'cimri.csv'

with open(file_name, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Sr.No', 'Laptop Name', 'Prices1', 'Prices2'])

    for i in range(len(Names)):
        writer.writerow([i, Names[i], Prices1[i], Prices2[i]])
        #print(i)
        #print(Names[i])
        #print(Prices1[i])