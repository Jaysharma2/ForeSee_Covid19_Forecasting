
# ForeSee Covid19 Forecasting


In response to the urgent need for timely and accurate information on the COVID-19 pandemic, the ForeSee Covid19 Forecasting system has been developed. This tool utilizes Time Series Forecasting techniques to predict the future spread of COVID-19 cases in India and its states. By providing reliable forecasts of case trends, ForeSee aims to support the government in implementing proactive measures to control and prevent the pandemic effectively.

### Video Demonstation:

<p align="center" width="100%">
<a href="https://drive.google.com/open?id=1-4WyJTzlZ0gmh8snkzrYf7cHcLBwR8SV"><img src="/images/VideoThumbnail.png" width="60%" align="center" >
</p>



## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Web App](#running-the-web-app)
  - [Training the Model and Getting Predictions](#training-the-model-and-getting-predictions)
- [Data Collection](#data-collection)
- [Data Pre-Processing](#data-pre-processing)
- [Model Creation and Evaluation](#model-creation-and-evaluation)
- [Predictions](#predictions)
- [Future Additions](#future-additions)
- [References](#references)
- [Team Members](#team-members)

## Overview

ForeSee Covid19 Forecasting uses an LSTM (Long Short-Term Memory) Multivariate Model for predicting future COVID-19 cases. The predictions include confirmed, recovered, and deceased cases, which are displayed in a web application built using the Python-Flask framework.

## Requirements

- Python 3.5 or 3.6+
- Python-Flask Framework
- numpy
- pandas
- matplotlib
- scikit-learn
- keras (with TensorFlow backend)

## Installation

To install the required dependencies, navigate to the main directory where `requirements.txt` is located and run:

```bash
pip install -r Team_SocioTechies_Samhar_Code/requirements.txt
```

Alternatively, you can install the required packages individually using:

```bash
pip install flask numpy pandas matplotlib scikit-learn
```

## Usage

### Running the Web App

1. Navigate to the `Team_SocioTechies_Samhar_Code` directory:

    ```bash
    cd Team_SocioTechies_Samhar_Code
    ```

2. Run the web app:

    ```bash
    python foresee_app.py
    ```

3. Open a web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view the application.

### Training the Model and Getting Predictions

1. To train the model and generate predictions, run the `train_country_states.py` file:

    ```bash
    python train_country_states.py
    ```

2. This script will call `train.py` and start training models for both country-wide and state-specific predictions. The predictions will be saved in the `/predictions` directory and will be reflected in the ForeSee Web App.

## Data Collection

Data for training the model is sourced from:

1. **India Predictions:**
   - [COVID19 India Org](https://api.covid19india.org/csv/): Provides time series data for Confirmed, Recovered, and Deceased Cases in India.
   - [Kaggle-COVID-19 Corona Virus India Dataset](https://www.kaggle.com/datasets): Contains state-wise case details.

2. **World Predictions:**
   - [CSSEGISandData](https://github.com/CSSEGISandData/COVID-19): Time series data for global COVID-19 cases.

## Data Pre-Processing

### Country India Dataset

- Divided into three files for Confirmed, Recovered, and Deceased cases.
- Rows with NaN values are removed.
- Growth factors are calculated for each date and stored in the `/country_data` directory.

### States Dataset

- Data is divided into files for each state.
- Rows with NaN values are removed.
- Growth factors are calculated and stored in the `/states_data` directory.

## Model Creation and Evaluation

The forecasting model uses an LSTM Multivariate Time Series Forecasting technique. The model is evaluated using Mean Absolute Error (MAE) and Mean Squared Error (MSE), with the Adam optimizer.

**Input Variables:**

- Number of Confirmed Cases
- Growth Factor for each date

**Growth Factor Calculation:**

- Growth Factor is the ratio of new cases on one day to cases on the previous day.

## Predictions

Predictions for future COVID-19 cases are generated for up to 7 days in advance and displayed on the ForeSee Web App. The app provides visualizations of predictions compared to actual case data.

## Future Additions

Future enhancements will include:

- **Weather Data:** Incorporating temperature and humidity data to assess impact on disease spread.
- **Social Data:** Using Twitter data for real-time updates on COVID-19 cases.
- **News Updates:** Web scraping news sites for event-based predictions.
- **Demographics:** Analyzing population demographics to refine predictions.

## References

- [Time Series Prediction Using Support Vector Machines](https://www.researchgate.net/publication/224408260_Time_Series_Prediction_Using_Support_Vector_Machines_A_Survey)
- [COVID19 India Org](https://api.covid19india.org/csv/)
- [CSSEGISandData](https://github.com/CSSEGISandData/COVID-19)
- [Multivariate Time Series Forecasting with LSTMs](https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/)
- [TensorFlow Time Series Tutorial](https://www.tensorflow.org/tutorials/structured_data/time_series#top_of_page)

