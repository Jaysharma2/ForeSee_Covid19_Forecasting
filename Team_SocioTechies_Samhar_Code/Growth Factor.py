import csv
import datetime
import os
import pandas as pd
import numpy as np

f1=open('country_data/India_Confirmed.csv','r')
reader=csv.reader(f1)
data=list(reader)
f1.close()
gr=['Growth Factor',0,0]
for i in range(len(data)):
	try:
		if i>2:
			gr.append((float(data[i][1])-float(data[i-1][1]))/(float(data[i-1][1])-float(data[i-2][1])))
	except:
		gr.append(0)
		continue
df= pd.read_csv("country_data/India_Confirmed.csv")

df["Growth Factor"] = np.array(gr[1:])
df=df.drop(['TEMP'],axis=1,errors='ignore')
df.to_csv('country_data/India_Confirmed.csv',index = False, header=True)

f1=open('country_data/India_Confirmed.csv','r')
reader=csv.reader(f1)
data=list(reader)  
f1=open('country_data/India_Confirmed.csv','r')
d1=f1.read()
last_date=datetime.datetime.strptime(data[-1][0],'%Y-%m-%d')
#print(last_date.date())
for i in range(1,8):
	if(i==1):
		d1=d1+str((last_date+datetime.timedelta(days = i)).strftime('%Y-%m-%d'))+',0,'+str(data[-1][2])
	else:
		d1=d1+'\n'+str((last_date+datetime.timedelta(days = i)).strftime('%Y-%m-%d'))+',0,'+str(data[-1][2])
f1.close()
f2=open('country_data/India_Confirmed_temp.csv','w')
f2.write(d1)
f2.close()