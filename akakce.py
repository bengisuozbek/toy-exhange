from bs4 import BeautifulSoup
import requests
import csv

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

source = requests.get('https://www.akakce.com/model-bebek.html', headers = headers).text
soup = BeautifulSoup(source, 'lxml')

# print(soup.prettify())

Names = []
Prices1 = []
#Prices2 = []

# for loop

for i in soup.find_all('h3', {'class':'pn_v8'}):
    string = i.text
    Names.append( string.strip() )

innerContent = soup.find('ul', class_="pl_v8 qv_v8")
li_items = innerContent.find_all('li', {'class':'w'})

for li in li_items:
    tags = li.find_all('span', class_='pt_v8')
    print("Li: ")
    print(li.text)

    for p in tags:
        print(p.text)
        if p.has_key('id'):
            if p['id'] == 'CPL':
                print(p.text)

for i in soup.find_all('span', class_='pt_v8'):
    text = i.text
    splitted = text.split("TL")
    print(splitted[0])

    Prices1.append(splitted[0])

    #for i in soup.find_all('span', class_='pt_v8'):
    #    Prices2.append(i.text)

        

######
#soup = BeautifulSoup(source.content, 'lxml') # parse according to html
#soup.find_all('li') #find required tags

#for i in range(len(soup.find_all('li'))):
#    print (soup.find_all('li')[i].get_text())


#for ultag in soup.find_all('ul'):
#    for li in ultag.find_all('li'):
#        i = soup.find_all('span', class_='pt_v8')
#        Prices2.append(i.text)
#        print(i)

#innerContent = soup.find('ul',class_="pl_v8 qv_v8")
#print(innerContent)

#li_items = innerContent.find_all('li', {'class':'w'})
num = len(li_items)
for x in range(num):
  print(x)


for li in li_items:
    #p_tags = li.find_all('span', class_='pt_v8') #The [:-1] removes the last p tag from the list, which is player__label

    tags = li.find_all('span', class_='pt_v8')
    for p in tags:
        print(p.text)
######



file_name = 'akakce.csv'

with open(file_name, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Sr.No', 'Name', 'Prices1'])

    for i in range(len(Names)):
        writer.writerow([i, Names[i], Prices1[i]])
        #print(i)
        #print(Names[i])
        #print(Prices1[i])

