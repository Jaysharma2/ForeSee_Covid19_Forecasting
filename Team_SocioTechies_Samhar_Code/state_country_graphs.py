import plotly.graph_objects as go
import pandas as pd


def draw_graphs():
	
	df_ic = pd.read_csv('predictions/India_Confirmed_Predictions.csv')
	df_ir = pd.read_csv('predictions/India_Recovered_Predictions.csv')
	df_id = pd.read_csv('predictions/India_Deceased_Predictions.csv')

	#df_in1 = pd.read_csv('country_data/India_Confirmed.csv')
	#df_in2 = pd.read_csv('country_data/India_Recovered.csv')
	#df_in3 = pd.read_csv('country_data/India_Deceased.csv')

	fig = go.Figure()
	fig.add_trace(go.Scatter(x = df_ic['Date'], y = df_ic['Predictions'],
	                  name='India Confirmed Cases Forecast',
	                  line=dict(color='purple', width=2)))

	fig.add_trace(go.Scatter(x = df_ir['Date'], y = df_ir['Predictions'],
	                  name='India Recovered Cases Forecast',
	                  line=dict(color='green', width=2)))

	fig.add_trace(go.Scatter(x = df_id['Date'], y = df_id['Predictions'],
	                  name='India Deceased Cases Forecast',
	                  line=dict(color='red', width=2)))

	fig.update_layout(title='India Confirmed Cases Forecast',
	                   plot_bgcolor='rgb(230, 230,230)',
	                   width=800,
    					height=300,
	                   showlegend=True,
	                    margin=dict(
				        l=0,
				        r=0,
				        b=0,
				        t=30,
				        pad=0
				    ))

	fig.write_html('templates/India_Conf_Pred.html')


	df_maha = pd.read_csv('predictions/Maharashtra_Confirmed_Predictions.csv')
	df_guj = pd.read_csv('predictions/Gujarat_Confirmed_Predictions.csv')
	df_raj = pd.read_csv('predictions/Rajasthan_Confirmed_Predictions.csv')

	fig2 = go.Figure()
	fig2.add_trace(go.Scatter(x = df_maha['Date'], y = df_maha['Predictions'],
	                  name='Maharashtra Confirmed Cases Forecast',
	                  line=dict(color='firebrick', width=2)))

	fig2.add_trace(go.Scatter(x = df_guj['Date'], y = df_guj['Predictions'],
	                  name='Gujarat Confirmed Cases Forecast',
					  line=dict(color='royalblue', width=2)))

	fig2.add_trace(go.Scatter(x = df_raj['Date'], y = df_raj['Predictions'],
	                  name='Rajasthan Confirmed Cases Forecast',
	                  line=dict(color='orange', width=2)))

	fig2.update_layout(title='State-Wise Confirmed Cases Forecast',
	                   plot_bgcolor='rgb(230, 230,230)',
	                   width=800,
    					height=300,
	                   showlegend=True,
	                    margin=dict(
				        l=0,
				        r=0,
				        b=0,
				        t=30,
				        pad=0
				    ))

	fig2.write_html('templates/States_Conf_Pred.html')


	df_age = pd.read_csv('age_group.csv')
	fig3 = go.Figure(data=[go.Bar(x=df_age['AGE_GROUP'], y=df_age['COUNT'],
	            hovertext=['Male:{0}\nFemale:{1}'.format(str(df_age['MALE'].iloc[0]),str(df_age['FEMALE'].iloc[0])),
	            			'Male:{0}\nFemale:{1}'.format(str(df_age['MALE'].iloc[1]),str(df_age['FEMALE'].iloc[1])),
	            			'Male:{0}\nFemale:{1}'.format(str(df_age['MALE'].iloc[2]),str(df_age['FEMALE'].iloc[2])),
	            			'Male:{0}\nFemale:{1}'.format(str(df_age['MALE'].iloc[3]),str(df_age['FEMALE'].iloc[3])),
	            			'Male:{0}\nFemale:{1}'.format(str(df_age['MALE'].iloc[4]),str(df_age['FEMALE'].iloc[4]))
	            			])])
	# Customize aspect
	fig3.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
	                  marker_line_width=1.5, opacity=0.6)
	fig3.update_layout(title_text='Age Group Report of COVID19 Affected Patients')
	fig3.write_html('templates/age_group_bar.html')


	df_mf = pd.read_csv('male_female_count.csv')
	labels = list(df_mf['GENDER'])
	values = list(df_mf['COUNT'])

	fig4 = go.Figure(data=[go.Pie(labels=labels, values=values)])
	fig4.update_layout(title_text='Population of Male and Female Affected',height=600,width=600)
	fig4.write_html('templates/mf_pie.html')



	fig5 = go.Figure(data=[go.Table(
				    header=dict(values=['India','Confirmed Forecast','Recoveries Forecast','Deceased Forecast'],
				                fill_color='paleturquoise',
				                align='center'),
				    cells=dict(values=[df_ic['Date'], df_ic['Predictions'],df_ir['Predictions'],df_id['Predictions']],
				               fill_color='lavender',
				               align='center'))
	])
	fig5.update_layout(title_text='India Cases Forecast')	
	fig5.write_html('templates/india_pred_table.html')


	fig6 = go.Figure(data=[go.Table(
				    header=dict(values=['Date','Maharashtra Confirmed Forecast','Gujarat Confirmed Forecast','Rajasthan Confirmed Forecast'],
				                fill_color='paleturquoise',
				                align='center'),
				    cells=dict(values=[df_maha['Date'], df_maha['Predictions'],df_guj['Predictions'],df_raj['Predictions']],
				               fill_color='lavender',
				               align='center'))
	])
	fig6.update_layout(title_text='States Confirmed Cases Forecast')	
	fig6.write_html('templates/states_pred_table.html')

	