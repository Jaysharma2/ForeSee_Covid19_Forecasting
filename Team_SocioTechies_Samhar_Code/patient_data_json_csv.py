import urllib.request
import json
out_data='SR.NO.,PATIENT NO,DATE ANNOUNCED,DETECTED STATE,AGE'
no=1
age_gp_0_10=0
age_gp_10_20=0
age_gp_20_30=0
age_gp_30_40=0
age_gp_40_50=0
age_gp_50_60=0
age_gp_60_70=0
age_gp_70_80=0
age_gp_80_90=0
age_gp_90_100=0
age_gp_0_10_male=0
age_gp_10_20_male=0
age_gp_20_30_male=0
age_gp_30_40_male=0
age_gp_40_50_male=0
age_gp_50_60_male=0
age_gp_60_70_male=0
age_gp_70_80_male=0
age_gp_80_90_male=0
age_gp_90_100_male=0
age_gp_0_10_female=0
age_gp_10_20_female=0
age_gp_20_30_female=0
age_gp_30_40_female=0
age_gp_40_50_female=0
age_gp_50_60_female=0
age_gp_60_70_female=0
age_gp_70_80_female=0
age_gp_80_90_female=0
age_gp_90_100_female=0
male=0
female=0
for i in range(1,5):
    print('Processing raw_data'+str(i))
    #f=open('d:/raw_data'+str(i)+'.json','r')
    #data=json.load(f)
    url=urllib.request.urlopen("https://api.covid19india.org/raw_data"+str(i)+".json")
    data = json.loads(url.read().decode())
    raw_data=data['raw_data']
    for i in raw_data:
        if i['gender']=='M':
            male=male+1
        if i['gender']=='F':
            female=female+1
        if i['agebracket']!='':
            #print((no,i['patientnumber'],i['dateannounced'],i['detectedstate'],i['agebracket']))
            out_data=out_data+'\n'+str(no)+','+i['patientnumber']+','+i['dateannounced']+','+i['detectedstate']+','+i['agebracket']
            try:
                if int(i['agebracket'])<10:
                    age_gp_0_10=age_gp_0_10+1
                    if i['gender']=='M':
                        age_gp_0_10_male=age_gp_0_10_male+1
                    if i['gender']=='F':
                        age_gp_0_10_female=age_gp_0_10_female+1
                elif int(i['agebracket'])<20:
                    age_gp_10_20=age_gp_10_20+1
                    if i['gender']=='M':
                        age_gp_10_20_male=age_gp_10_20_male+1
                    if i['gender']=='F':
                        age_gp_10_20_female=age_gp_10_20_female+1
                elif int(i['agebracket'])<30:
                    age_gp_20_30=age_gp_20_30+1
                    if i['gender']=='M':
                        age_gp_20_30_male=age_gp_20_30_male+1
                    if i['gender']=='F':
                        age_gp_20_30_female=age_gp_20_30_female+1
                elif int(i['agebracket'])<40:
                    age_gp_30_40=age_gp_30_40+1
                    if i['gender']=='M':
                        age_gp_30_40_male=age_gp_30_40_male+1
                    if i['gender']=='F':
                        age_gp_30_40_female=age_gp_30_40_female+1
                elif int(i['agebracket'])<50:
                    age_gp_40_50=age_gp_40_50+1
                    if i['gender']=='M':
                        age_gp_40_50_male=age_gp_40_50_male+1
                    if i['gender']=='F':
                        age_gp_40_50_female=age_gp_40_50_female+1
                elif int(i['agebracket'])<60:
                    age_gp_50_60=age_gp_50_60+1
                    if i['gender']=='M':
                        age_gp_50_60_male=age_gp_50_60_male+1
                    if i['gender']=='F':
                        age_gp_50_60_female=age_gp_50_60_female+1
                elif int(i['agebracket'])<70:
                    age_gp_60_70=age_gp_60_70+1
                    if i['gender']=='M':
                        age_gp_60_70_male=age_gp_60_70_male+1
                    if i['gender']=='F':
                        age_gp_60_70_female=age_gp_60_70_female+1
                elif int(i['agebracket'])<80:
                    age_gp_70_80=age_gp_70_80+1
                    if i['gender']=='M':
                        age_gp_70_80_male=age_gp_70_80_male+1
                    if i['gender']=='F':
                        age_gp_70_80_female=age_gp_70_80_female+1
                elif int(i['agebracket'])<90:
                    age_gp_80_90=age_gp_80_90+1
                    if i['gender']=='M':
                        age_gp_80_90_male=age_gp_80_90_male+1
                    if i['gender']=='F':
                        age_gp_80_90_female=age_gp_80_90_female+1
                elif int(i['agebracket'])<100:
                    age_gp_90_100=age_gp_90_100+1
                    if i['gender']=='M':
                        age_gp_90_100_male=age_gp_90_100_male+1
                    if i['gender']=='F':
                        age_gp_90_100_female=age_gp_90_100_female+1
            except:
                #print('age is not an int \n age = ')
                #print(i['agebracket'])
                if i['agebracket']=='28-35':
                    age_gp_30_40=age_gp_30_40+1
                elif float(i['agebracket'])<10:
                    age_gp_0_10=age_gp_0_10+1
                elif float(i['agebracket'])<30:
                    age_gp_20_30=age_gp_20_30+1
                continue
            no=no+1
out_data=out_data+'\n\n\n\n'+'AGE_GROUP,'+'age_gp_0_20,'+'age_gp_20_40,'+'age_gp_40_60,'+'age_gp_60_80,'+'age_gp_80_100\n'+'COUNT,'+str(age_gp_0_10+age_gp_10_20)+','+str(age_gp_20_30+age_gp_30_40)+','+str(age_gp_40_50+age_gp_50_60)+','+str(age_gp_60_70+age_gp_70_80)+','+str(age_gp_80_90+age_gp_90_100)+'\nPERCENTAGE,'+str((age_gp_0_10*100/no)+(age_gp_10_20*100/no))+','+str((age_gp_20_30*100/no)+(age_gp_30_40*100/no))+','+str((age_gp_40_50*100/no)+(age_gp_50_60*100/no))+','+str((age_gp_60_70*100/no)+(age_gp_70_80*100/no))+','+str((age_gp_80_90*100/no)+(age_gp_90_100*100/no))+'\nMALE,'+str((age_gp_0_10_male)+(age_gp_10_20_male))+','+str((age_gp_20_30_male)+(age_gp_30_40_male))+','+str((age_gp_40_50_male)+(age_gp_50_60_male))+','+str((age_gp_60_70_male)+(age_gp_70_80_male))+','+str((age_gp_80_90_male)+(age_gp_90_100_male))+'\nFEMALE,'+str((age_gp_0_10_female)+(age_gp_10_20_female))+','+str((age_gp_20_30_female)+(age_gp_30_40_female))+','+str((age_gp_40_50_female)+(age_gp_50_60_female))+','+str((age_gp_60_70_female)+(age_gp_70_80_female))+','+str((age_gp_80_90_female)+(age_gp_90_100_female))+'\n\n\n\n\nGENDER,'+'MALE'+','+'FEMALE\nCOUNT,'+str(male)+','+str(female)+'\nPERCENTAGE,'+str(male*100/(male+female))+','+str(female*100/(male+female))

f1=open('out_data.csv','w')
f1.write(out_data)
f1.close()
print('data at /out_data.csv')
