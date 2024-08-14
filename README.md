# ForeSee Covid19 Forecasting


In response to the urgent need for timely and accurate information on the COVID-19 pandemic, the ForeSee Covid19 Forecasting system has been developed. This tool utilizes Time Series Forecasting techniques to predict the future spread of COVID-19 cases in India and its states. By providing reliable forecasts of case trends, ForeSee aims to support the government in implementing proactive measures to control and prevent the pandemic effectively.

[<img src="/images/ForeSee_dash.png" width="50%">](https://drive.google.com/open?id=1-4WyJTzlZ0gmh8snkzrYf7cHcLBwR8SV "Demonstartion Video")

### Requirements:
* Python 3.5 or 3.6+
* Python-Flask Framework
* numpy  
* pandas 
* plotly
* scikit-learn
* keras - with tensorflow backend


``` 
pip install flask
```
``` 
pip install numpy
```
```
pip install pandas
```
```
pip install matplotlib
```
```
pip install scikit-learn
```
For installing all the required modules, run the given command from the main directory having the requirements.txt file,
```
pip install -r requirements.txt
```
### Steps to Run the Code:

Steps to run the web app:
1.  Go to the directory Team_SocioTechies_Samhar_Code,
2.  Run the web app,
```
python foresee_app.py 
```
3.	Copy the http://127.0.0.1:5000/ address to the browser as localhost.

### Steps to train the model and get Predictions:
1.	Run the train_country_states.py file
```
python train_country_states.py
```
2.	This calls the main file train.py and training starts for both the country and the states models.
3.	The predictions after training are stored in /predictions directory.
4.	These predictions are stored separately for each of the state and the country as Confirmed, Recovered and Deceased cases respectively.
These changes are reflected on the ForeSee Web App.

### Data Collection:
For training the model, the datasets have been taken from two sources.
#### 1. Dataset for India Predictions
The dataset is taken from [COVID19 India Org](https://api.covid19india.org/csv/latest/case_time_series.csv) (This link will download the csv file for India's Case Time Series).
This source provides time series data for Confirmed, Recovered and Deceased Cases of COVID-19 in India daily.

#### 2. Dataset for India-States Prediction
The dataset is taken from [Kaggle-COVID-19 Corona Virus India Dataset](https://www.kaggle.com/imdevskp/covid19-corona-virus-india-dataset). The file containing state-wise details of cases can be seen [here](https://github.com/imdevskp/covid-19-india-data/blob/master/complete.csv).

##### Note: We have modified the dataset according to the requirements for getting best results. 

### Data Pre-Processing

#### Country India Dataset Pre-Processing
1. The data collected from COVID19 India Org is divided into three different files containing the number of Total Confirmed, Total Recovered and Total Deceased cases respectively.
2. The rows with NaN values if any, are dropped and the datasets for training are stored in the directory /country_data.
3. Then for each of these datasets, corresponding growth factor is calculated for each date.

#### States Dataset Pre-Processing
1. The data collected from Kaggle-COVID-19 Corona Virus India Dataset is divided into separate files categorizing the data based on different states. These datasets contain the number of Total Confirmed, Total Recovered and Total Deceased cases for each state.
2. The rows with NaN values if any, are dropped and the datasets for training are stored in the directory /states_data.
3. Then for each of these datasets, corresponding growth factor is calculated for each date.

### Model Creation and Evaluation
The forecasting model is made using LSTM Multivariate Time Series Forecasting. This is suitable for non-linear regression problem similar to the spread of COVID-19 disease. LSTM learns non-linearity from the data and as the data increases, it learns better and the predictions can get improved. 

The model is evaluated using 'MAE' (Mean Absolute Error) and 'MSE' (Mean Squared Error) and optimizer used is 'Adam'.

The dataset comprises of two input variables which are, 
1. The Number of Confirmed Cases
2. The Growth Factor for each date

#### Growth Factor
Growth Factor is defined as the ratio between the number of new cases on one day, and the number of cases the previous day.
It is calculated by using the given formula,
![growth_factor](https://raw.githubusercontent.com/CodensureLetsCode/ForeSee_Covid19_Forecasting/master/images/growth_factor.png)

Growth factor for each day was calculated, and it showed a good improvement in predictions.

The model predicts the future number of cases for the next 7 days. The Actual Confirmed Cases and the Predicted Confirmed Cases for India from 16th May to 24th May can be seen in the figure below,

![Predictions](https://raw.githubusercontent.com/CodensureLetsCode/ForeSee_Covid19_Forecasting/master/images/predictions.png)

The graph for the above predictions can be seen below,

![PredictionPlot](https://raw.githubusercontent.com/CodensureLetsCode/ForeSee_Covid19_Forecasting/master/images/pred_gragh.png)

After testing the predictions for the known dates and values, the model was given the future dates for making the predictions further from 25th May to 31st May, the results of the Confirmed Cases of India is shown in the table below,

![IndiaPredictions](https://raw.githubusercontent.com/CodensureLetsCode/ForeSee_Covid19_Forecasting/master/images/India_pred_7days.png)

These predictions are displayed on the Web Application 'ForeSee' made using Python-Flask Framework.

Further we have compared the future predictions for 25th May with the actual cases reached that day, and the comparison is given below, where the actual cases are taken from the live update of India Confirmed Cases.

Actual Number of Confirmed Cases             | Future Predictions made for 25th May 
:-------------------------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/CodensureLetsCode/ForeSee_Covid19_Forecasting/master/images/source_data.png)                     |  ![](https://raw.githubusercontent.com/CodensureLetsCode/ForeSee_Covid19_Forecasting/master/images/comparison_pred.png)

#### The Web App 'ForeSee'
![ForeSee](https://raw.githubusercontent.com/CodensureLetsCode/ForeSee_Covid19_Forecasting/master/images/ForeSee_dash.png)


#### NEWS Alerts
There is a sudden increase in the events taking place all over the country due to the panic created by COVID-19. These events may include any social or political gathering, making goods available to the public in some areas, large migrations of people, etc. These events can cause an increase in the number of interactions among people and can lead to the spread of the disease at a much faster pace. These events are mostly updated very frequently on news sites. The trusted news sites can be used to extract information from future events and make predictions about the increase in transmission of the disease. This feature can add more weightage to the predicted number of confirmed cases for future dates. 

Web Scraping – The news articles are retrieved as using specific keywords from trustworthy sites by Web Scraping using Python. Python provides the most efficient and quickest way to extract the textual data from news articles using the BeautifulSoup library and requests module. The extracted titles are stored in a CSV file along with the timestamps. This data is displayed on web app as news updates.

* This feature is yet to be improved by adding a language model for Natural Language Processing and determining the context of the news or social data.
Let's say this step as Context Classification. This will be of great use when we want to predict the increase in number of cases that can occur  

Examples of the events in case of COVID-19 can be: 
* Violation of Lockdown
* Social Gathering
* Difficulties to Hospitals in giving treatment
* Indian Markets Functioning 

The application ‘ForeSee’ will cover all the possible cases to predict the spread of COVID-19 in future dates and will enable early detection and prevention of the disease in the country.

### References:
1. https://www.researchgate.net/publication/224408260_Time_Series_Prediction_Using_Support_Vector_Machines_A_Survey
2. https://api.covid19india.org/csv/
3. https://github.com/CSSEGISandData/COVID-19
4. https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/
5. https://www.tensorflow.org/tutorials/structured_data/time_series#top_of_page

#### Team Members:
##### Aditi Sharma
##### Himanshu Sen
##### Jay Sharma
