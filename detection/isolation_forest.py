import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(data, contamination=0.2): #  expect ~ 2% of anomalies
    
    x = data[['request_count',
        'unique_endpoints',
        'mean_time_diff',
        'std_time_diff',
        'error_rate',
        'rare_endpoint_ratio',
        'avg_response_size',
        'response_size_std']]
    
    iso_forest = IsolationForest(contamination=contamination
                                ,random_state=42,
                                n_estimators=200)
    data['anomalies'] = iso_forest.fit_predict(x)
    data['anomaly_flag'] = data['anomalies'].map({1: False, -1: True})
    return data['anomalies']
"""
if __name__ == "__main__":
    features = pd.read_csv("data/engineered_features.csv", parse_dates=["timestamp"])
    features_with_anomalies = detect_anomalies(features)
    print(features_with_anomalies.value_counts())
    print("\n--- Sample anomalies ---")
    print(features[features_with_anomalies == -1].head())"""