from train import state_data_preprocess
from train import perform_state_predictions
from train import save_predictions
from train import country_data_preprocess
from train import perform_country_predictions
import time

start_time = time.time()
train_country = 'no'
train_states='yes'
if(train_states=='yes'):
    states = ['Maharashtra','Gujarat','Rajasthan']
    cases = ['Confirmed','Deceased']
    for st in states:
        for typ in cases:
            state_data_preprocess(st,typ)
            pred_dates, pred = perform_state_predictions(st,typ)
            print(pred)
            print(pred_dates)
            save_predictions(pred_dates,pred,st,typ)
            print("----------------------------------------- %s seconds ------------------------------------------" % (time.time() - start_time))

elif(train_country=='yes'):
    countries = ['India']
    country_cases = ['Confirmed','Recovered','Deceased']
    for c in countries:
        country_data_preprocess(c)
        for typ in country_cases:
            pred_dates, pred = perform_country_predictions(c,typ)
            print(pred)
            print(pred_dates)
            save_predictions(pred_dates,pred,c,typ)
            print("----------------------------------------- %s seconds ------------------------------------------" % (time.time() - start_time))
