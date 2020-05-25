import warnings
warnings.filterwarnings("ignore")
from math import sqrt
from numpy import concatenate
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import datetime
import csv
import os


def state_data_preprocess(state,casestype):
	state = state
	casestype=casestype
	# load dataset
	dataset = pd.read_csv('https://raw.githubusercontent.com/imdevskp/covid-19-india-data/master/complete.csv', header=0, index_col=0)
	df_state = dataset[dataset['Name of State / UT']==state]
	df_state = df_state.dropna() 
	
	if(casestype=='Confirmed'):
		df_state =  df_state.drop(['Total Confirmed cases (Indian National)', 'Total Confirmed cases ( Foreign National )', 'Cured/Discharged/Migrated', 'Latitude', 'Longitude', 'Death'], axis=1)
		df_state.index = pd.to_datetime(df_state.index)
		df_state = df_state[['Total Confirmed cases','Name of State / UT']]
		df_state.columns = ['Total Confirmed Cases','State']


	elif(casestype=='Deceased'):
		df_state =  df_state.drop(['Total Confirmed cases (Indian National)', 'Total Confirmed cases ( Foreign National )', 'Cured/Discharged/Migrated', 'Latitude', 'Longitude','Total Confirmed cases'], axis=1)
		df_state.index = pd.to_datetime(df_state.index)
		df_state = df_state[['Death','Name of State / UT']]
		df_state.columns = ['Total Deceased Cases','State']
	
	df_state.to_csv('states_data/{0}_{1}.csv'.format(state,casestype))
	
	f1=open('states_data/{0}_{1}.csv'.format(state,casestype),'r')
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
	df= pd.read_csv('states_data/{0}_{1}.csv'.format(state,casestype))

	df["Growth Factor"] = np.array(gr[1:])
	df=df.drop(['TEMP'],axis=1,errors='ignore')
	df.to_csv('states_data/{0}_{1}.csv'.format(state,casestype),index = False, header=True)

	f1=open('states_data/{0}_{1}.csv'.format(state,casestype),'r')
	reader=csv.reader(f1)
	data=list(reader)
	f1=open('states_data/{0}_{1}.csv'.format(state,casestype),'r')
	d1=f1.read()
	d1=d1.rstrip()
	last_date=datetime.datetime.strptime(data[-1][0],'%Y-%m-%d')
	#print(last_date.date())
	for i in range(1,8):
	    d1=d1+'\n'+str((last_date+datetime.timedelta(days = i)).strftime('%d-%m-%Y'))+',0,'+str(data[-1][2])
	f1.close()
	f2=open('states_data/{0}_{1}_temp.csv'.format(state,casestype),'w')
	f2.write(d1)
	f2.close()
	#dataset = pd.read_csv('states_data/{0}_{1}_temp.csv'.format(state,casestype), header=0, index_col=0)
	#os.remove('states_data/{0}_{1}_temp.csv'.format(state,casestype))


# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


def perform_state_predictions(state,casestype):
	state = state
	casestype = casestype
	df_dataset = pd.read_csv('states_data/{0}_{1}_temp.csv'.format(state,casestype), header=0, index_col=0)
	df_dataset = df_dataset.drop(['State'],axis=1)
	df_dataset = df_dataset.dropna()
	values = df_dataset.values
	encoder = LabelEncoder()
	#values[:,2] = encoder.fit_transform(values[:,2])
	values = values.astype('float32')
	# normalize features
	scaler = MinMaxScaler(feature_range=(0, 1))
	scaled = scaler.fit_transform(values)
	
	reframed = series_to_supervised(scaled, 1, 1)
	reframed.drop(reframed.columns[[3]], axis=1, inplace=True)
	#print(reframed.head())
	
	values = reframed.values
	
	n_train_rows = len(df_dataset)-10
	train = values[:n_train_rows, :]
	test = values[n_train_rows:, :]

	train_X, train_y = train[:, :-1], train[:, -1]
	test_X, test_y = test[:, :-1], test[:, -1]

	train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
	test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
	#print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

	model = Sequential()
	model.add(LSTM(80, input_shape=(train_X.shape[1], train_X.shape[2])))
	model.add(Dense(1))
	model.compile(loss='mse', optimizer='adam')

	history = model.fit(train_X, train_y, epochs=80, batch_size=1, validation_data=(test_X, test_y), verbose=2, shuffle=False)
	#yhat = model.predict(test_X)
	tcase=test_X[:-6]
	for i in range(6,0,-1):
	    yhat = model.predict(tcase)
	    tcase=np.append(tcase,np.array([[[float(yhat[-1]) , float(test_X[-1][0][1])]]]),axis=0)
	yhat = model.predict(tcase)
	test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))

	tcase = tcase.reshape((test_X.shape[0], test_X.shape[1])).astype('float32')

	inv_yhat = concatenate((yhat, tcase[:, 1:]), axis=1)
	inv_yhat = scaler.inverse_transform(inv_yhat)
	inv_yhat = inv_yhat[:,0]

	test_y = test_y.reshape((len(test_y), 1))
	inv_y = concatenate((test_y, tcase[:, 1:]), axis=1)
	inv_y = scaler.inverse_transform(inv_y)
	inv_y = inv_y[:,0]

	rmse = sqrt(mean_squared_error(inv_y, inv_yhat))

	df_dataset.index = pd.to_datetime(df_dataset.index)
	dates = []
	for timestamp in list(df_dataset.index):
	    dates.append(datetime.datetime.strftime(timestamp.date(),'%y{}-%m-%d'.format('20')))
	#print(dates)

	pred_dates = dates[-7:]

	state_predictions = []
	for i in range(2,inv_yhat.shape[0]):
	    print(inv_y[i],inv_yhat[i])
	    state_predictions.append(round(inv_yhat[i]))
	
	return(pred_dates,state_predictions)



def save_predictions(pred_dates,predictions,state,casestype):
	predictions = predictions
	pred_dates = pred_dates
	state = state
	casestype = casestype
	df_pred = pd.DataFrame({'Predictions':predictions},index=pred_dates)
	df_pred.index.name = 'Date' 
	df_pred.to_csv('predictions/{0}_{1}_Predictions.csv'.format(state,casestype))


'''state_data_preprocess('Maharashtra')
pred_dates, pred = perform_predictions('Maharashtra','Confirmed')

print(pred)
print(pred_dates)

save_predictions(pred_dates,pred,'Maharashtra','Confirmed')
'''

def country_data_preprocess(country):
	country=country
	dataset = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv', header=0, index_col=0)
	dataset=dataset.dropna()
	month = {'January':'01',
        'February':'02',
        'March':'03',
		'April':'04',
		'May':'05',
		'June':'06',
		'July':'07',
		'August':'08',
		'September':'09',
		'October':'10',
		'November':'11',
		'December':'12'}

	new_dates = []
	for dt in dataset.index.values:
		new_date = '2020-'+str(month[dt[3:-1]])+'-'+dt[:2]
		new_dates.append(new_date)
	#print(new_dates)

	dataset.index = pd.to_datetime(new_dates)
	dataset.index.name = 'Date'
	df_confirmed, df_recovered, df_deceased = pd.DataFrame(dataset), pd.DataFrame(dataset), pd.DataFrame(dataset)
	df_confirmed = df_confirmed.drop(['Daily Confirmed', 'Daily Recovered','Total Recovered', 'Daily Deceased', 'Total Deceased'], axis=1)
	df_recovered = df_recovered.drop(['Daily Confirmed', 'Daily Recovered','Total Confirmed', 'Daily Deceased', 'Total Deceased'], axis=1)
	df_deceased = df_deceased.drop(['Daily Confirmed', 'Daily Recovered','Total Recovered', 'Daily Deceased', 'Total Confirmed'], axis=1)

	df_confirmed_final.to_csv('country_data/India_Confirmed.csv')
	df_recovered_final.to_csv('country_data/India_Recovered.csv')
	df_deceased_final.to_csv('country_data/India_Deceased.csv')


	country = ['India']
	cases = ['Confirmed','Recovered','Deceased']
	for c in country:
		for case in cases:
			f1=open('country_data/{0}_{1}.csv'.format(c,case),'r')
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
			df= pd.read_csv('country_data/{0}_{1}.csv'.format(c,case))

			df["Growth Factor"] = np.array(gr[1:])
			df=df.drop(['TEMP'],axis=1,errors='ignore')
			df.to_csv('country_data/{0}_{1}.csv'.format(c,case),index = False, header=True)

			f1=open('country_data/{0}_{1}.csv'.format(c,case),'r')
			reader=csv.reader(f1)
			data=list(reader)
			f1=open('country_data/{0}_{1}.csv'.format(c,case),'r')
			d1=f1.read()
			d1=d1.rstrip()
			last_date=datetime.datetime.strptime(data[-1][0],'%Y-%m-%d')
			#print(last_date.date())
			for i in range(1,8):
			    d1=d1+'\n'+str((last_date+datetime.timedelta(days = i)).strftime('%d-%m-%Y'))+',0,'+str(data[-1][2])
			f1.close()
			f2=open('country_data/{0}_{1}_temp.csv'.format(c,case),'w')
			f2.write(d1)
			f2.close()
			#dataset = pd.read_csv('country_data/{0}_{1}_temp.csv'.format(c,case), header=0, index_col=0)
			#os.remove('country_data/{0}_{1}_temp.csv'.format(c,case))



def perform_country_predictions(country,casestype):
	country = country
	casestype = casestype
	dataset = pd.read_csv('country_data/{0}_{1}_temp.csv'.format(country,casestype), header=0, index_col=0)
	values = dataset.values
	values = values.astype('float32')
	scaler = MinMaxScaler(feature_range=(0, 1))
	scaled = scaler.fit_transform(values)
	reframed = series_to_supervised(scaled, 1, 1)
	reframed.drop(reframed.columns[[3]], axis=1, inplace=True)
	
	# split into train and test sets
	values = reframed.values
	n_train_rows = len(dataset)-10
	train = values[:n_train_rows, :]
	test = values[n_train_rows:, :]

	# split into input and outputs
	train_X, train_y = train[:, :-1], train[:, -1]
	test_X, test_y = test[:, :-1], test[:, -1]

	train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
	test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
	#print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

	# design network
	model = Sequential()
	model.add(LSTM(80, input_shape=(train_X.shape[1], train_X.shape[2])))
	model.add(Dense(1))
	model.compile(loss='mse', optimizer='adam')

	history = model.fit(train_X, train_y, epochs=80, batch_size=1, validation_data=(test_X, test_y), verbose=2, shuffle=False)

	# make a prediction
	#yhat = model.predict(test_X)
	tcase=test_X[:-6]
	for i in range(6,0,-1):
	    yhat = model.predict(tcase)
	    tcase=np.append(tcase,np.array([[[float(yhat[-1]) , float(test_X[-1][0][1])]]]),axis=0)
	yhat = model.predict(tcase)
	test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))

	tcase = tcase.reshape((test_X.shape[0], test_X.shape[1])).astype('float32')

	inv_yhat = concatenate((yhat, tcase[:, 1:]), axis=1)
	inv_yhat = scaler.inverse_transform(inv_yhat)
	inv_yhat = inv_yhat[:,0]

	test_y = test_y.reshape((len(test_y), 1))
	inv_y = concatenate((test_y, tcase[:, 1:]), axis=1)
	inv_y = scaler.inverse_transform(inv_y)
	inv_y = inv_y[:,0]

	rmse = sqrt(mean_squared_error(inv_y, inv_yhat))

	pred_dates = list(dataset.index)[-7:]

	country_predictions = []
	for i in range(2,inv_yhat.shape[0]):
	    print(inv_y[i],inv_yhat[i])
	    country_predictions.append(round(inv_yhat[i]))
	print(country_predictions)

	return(pred_dates,country_predictions)




