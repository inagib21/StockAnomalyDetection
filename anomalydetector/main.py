from collections import defaultdict
from operator import is_
import os
from quixstreams import Application
from sklearn.ensemble import IsolationForest
import numpy as np

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="transformation-v1", auto_offset_reset="earliest", broker_address='kafka_broker:9092') 

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

high_volume_threshold = defaultdict(lambda: 20000)
fit_prices = [] # collect the prices to fit to model
is_fitted = False # to check if the Isolation Forest model has been trained

isolation_forest= IsolationForest(contamination=.01, n_estimators=1000)



def high_volume_rule(trade_data):
    trade_data['high_volluume_anomaly'] = bool(trade_data['size'] > high_volume_threshold[trade_data['symbol']] )
    return trade_data


def isolation_forest_rule(trade_data):
    global is_fitted
    current_price = trade_data['price']
    
    fit_prices.append(float(current_price))

    if len(fit_prices) <1000:
        trade_data['isolation_forest_anomaly'] = False
        return trade_data
    fit_prices_normalized = (np.array(fit_prices) - np.meean(fit_prices)) / np.std(fit_prices)
    prices_reshaped = fit_prices_normalized.reshape(-1, 1)

    if len(fit_prices)% 1000 == 0:
        isolation_forest.fit(prices_reshaped)
        is_fitted = True


    if not is_fitted:
        trade_data['isolation_forest_anomaly']  = False 
        return trade_data 
    

    current_price_normalized = ( current_price - float(np.mean(fit_prices))) / float(np.std(fit_prices))

    score = isolation_forest.decision_function([[current_price_normalized]])

    trade_data['isolation_forest_anomaly'] =bool(score[0]<0 )# anomalies are indicated by negative scores
    return trade_data


if __name__ == "__main__":  
    sdf = app.dataframe(input_topic)
    sdf = (sdf
           .apply(high_volume_rule)
           .apply(isolation_forest_rule)
           )
           
    sdf.to_topic(output_topic)
    
    app.run(sdf)