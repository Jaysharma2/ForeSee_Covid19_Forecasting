from flask import Flask,url_for,redirect,render_template, request,send_from_directory
from state_country_graphs import draw_graphs
import pandas as pd
import numpy as np
import time
app = Flask(__name__)
import sys

sys.path.append("..")

from urllib.request import urlopen
from bs4 import BeautifulSoup
import newspaper
import csv


def collect_news_updates():

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



@app.route("/")
def display_pred():
    #collect_news_updates()
    draw_graphs()
    latest=[]
    states = ['Maharashtra','Gujarat','Rajasthan']
    cases = ['Confirmed','Deceased']
    predictions={}
    for st in states:
        predt=[]
        df_predt = pd.read_csv('predictions/{0}_Confirmed_Predictions.csv'.format(st))
        predt = list(df_predt['Predictions'])
        predictions[st] = predt
    print(predictions)

    df_total = pd.read_csv("https://api.covid19india.org/csv/latest/case_time_series.csv")
    latest.append(int(df_total['Total Confirmed'].iloc[-1]))
    latest.append(int(df_total['Total Recovered'].iloc[-1]))
    latest.append(int(df_total['Total Deceased'].iloc[-1]))

    df_india = pd.read_csv('country_data/India_Confirmed.csv')
    latest_date = df_india['Date'].iloc[-1]


    df_news = pd.read_csv('Extracted_news_data.csv',encoding='latin1')
    news_updates = list(df_news['HEADLINE'])
    cities = list(df_news['CITY'])
    news = {}
    for i in range(len(news_updates)):
        news[cities[i].capitalize()] = news_updates[i]  

    #time.sleep(10)
    return render_template('home.html',predictions=predictions,latest=latest,latest_date=latest_date,news=news)

@app.route("/plot1")
def india_pred():
    return render_template('India_Conf_Pred.html')

@app.route("/plot2")
def states_pred():
    return render_template('States_Conf_Pred.html')

@app.route("/plot3")
def age_grp():
    return render_template('age_group_bar.html')

@app.route("/plot4")
def mf_count():
    return render_template('mf_pie.html')

@app.route("/plot5")
def india_table():
    return render_template('india_pred_table.html')

@app.route("/plot6")
def state_table():
    return render_template('states_pred_table.html')



if __name__ == '__main__':
    
    app.run(debug=True)