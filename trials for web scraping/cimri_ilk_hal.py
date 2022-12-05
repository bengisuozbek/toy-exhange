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


#for i in price_content:
#    Prices1.append(i.text)


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
        #splitted_1 = price.split(".com")
        # s = splitted_1.[1]
        #print(splitted_1[0])

        #x1 = splitted_1[1].split(".tr")
        #splitted_2 = s.split("com")
        #print(x1)

        #x2 = x1[0].split("TL")
        #splitted_2 = s.split("com")
        #print(x2)

        #x3 = x2[0].split("TL")
        #splitted_2 = s.split("com")
        #print(x3)
        
        if(index == 0):
            price = i.get_text()
            splitted_1 = price.split(".com")
            # s = splitted_1.[1]
            #print(split-ted_1[0])

            x1 = splitted_1[1].split(".tr")
            #splitted_2 = s.split("com")
            #print(x1)

            x2 = x1[0].split("TL")
            #splitted_2 = s.split("com")
            #print(x2)

            #Prices1.append(x2[0])
            print(x2[0])
            Prices1.append(x2[0])
            index += 1
        if(index == 1):
            Prices2.append(i.get_text())
            index = 0



imageContent = []

url = 'https://www.cimri.com/oyuncak-bebekler'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

img = soup.find('div', 's1cegxbo-1 cACjAF')
images = img.find_all('img')

#print(images)

for image in images:
    name = image['alt']
    link = image['src']
    print(name, link)

    for name in Names:
        if(name == image['alt']):
            imageContent.append(link.strip())


# ##
# toy_image = []
# for toy_name in Names:
#     for img in imageContent:
#         if(img == toy_name):
#             toy_image.append(img['alt'])
#             print('SAME')
# #


file_name = 'cimri1111.csv'



with open(file_name, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Sr.No', 'Name', 'Prices1', 'Prices2', 'image'])

    for i in range(len(imageContent)):
        writer.writerow([i, Names[i], Prices1[i], Prices2[i], imageContent[i]])
        #print(i)
        #print(Names[i])
        #print(Prices1[i])

# IMAGE WEB SCRAPING :

#https://www.cimri.com/oyuncak-bebekler/en-ucuz-barbie-fhy73-barbienin-ruya-evi-fiyatlari,403103312

# def getdata(url): 
#     r = requests.get(url) 
#     return r.text 
    
# htmldata = getdata("https://www.cimri.com/oyuncak-bebekler/en-ucuz-barbie-fhy73-barbienin-ruya-evi-fiyatlari,403103312") 
# soup = BeautifulSoup(htmldata, 'html.parser') 
# b = 0
# for item in soup.find_all('img'):
#     b += 1
#     print('b', b)
#     print(item['src'])


# def getdata(url): 
#     r = requests.get(url) 
#     return r.text 
    
# htmldata = getdata("https://www.cimri.com/oyuncak-bebekler/en-ucuz-barbie-fhy73-barbienin-ruya-evi-fiyatlari,403103312") 
# soup = BeautifulSoup(htmldata, 'html.parser') 
# images = []
# imageContent = soup.find('li', class_="s1wxq1uo-2 iVTokt")
# i= 0
    
# print(i) 

# image_content = imageContent.find_all('img', {'class':'s51lp5-0 iRZUoF initial loading'})


# for item in image_content:
#     i += 1
#     print(i) 
#     string = i.text
#     images.append( string.strip() )

# # for item in soup.find_all('div', {'class':'m50b2p-0 iHtcZy'}):
# #     for images in soup.find_all('img'):
# #         print(images['src'])


# print(i)
# for item in soup.find_all('img', {'class':'s51lp5-0 cRlUpX loaded'}):
#     i += 1
#     print(i) 
#     print(item['src'])