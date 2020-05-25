from urllib.request import urlopen
from bs4 import BeautifulSoup
import newspaper
import csv

source_site="https://timesofindia.indiatimes.com/topic/Public-Gathering"

html = urlopen(source_site)
bsObj = BeautifulSoup(html.read(),features="lxml");

lks=[]

for link in bsObj.find_all('a'):
    s=str(link.get('href'))
    if 'gather' in s:
        if 'city' in s:
            #print(link.get('href'))
            lks.append(str(link.get('href')))
summary='DATE,URL,SUMMARY,CITY,HEADLINE'
for i in lks:
    print(source_site[:-23]+i)
    url=source_site[:-23]+i
    article=newspaper.Article(url)
    #print(article.publish_date)
    article.download()
    d=article.html.split('IST')[0].split('|')
    #print(d[-1])
    h=article.html.split('<title>')[1].split('</title>')[0]
    print(h)
    article.parse()
    article.nlp()
    places = i.split('/')
    summary = summary+'\n'+d[-1].replace(',','')+'IST'+','+url+','+article.summary.replace('\n','').replace(',',' | ')+','+str(places[2])+','+h.replace(',','')
    #print(summary)

f=open('Extracted_news_data.csv','w')
f.write(summary)
f.close()
