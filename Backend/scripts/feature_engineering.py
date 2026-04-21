import pandas as pd
import numpy as np

def feature_engineering(path, window="1min"):

    # Load CSV
    df = pd.read_csv(path, parse_dates=["time"])

    # Rename for consistency
    df.rename(columns={"time": "timestamp"}, inplace=True)

    # Sort logs
    df = df.sort_values(by="timestamp")

    # Time difference between requests from same IP
    df["time_diff"] = df.groupby("ip")["timestamp"].diff().dt.total_seconds()

    # Rare endpoint detection
    endpoint_freq = df["endpoint"].value_counts(normalize=True)
    df["is_rare_endpoint"] = df["endpoint"].map(endpoint_freq) < 0.01
    
    # Window aggregation
    agg = df.groupby(
        ["ip", pd.Grouper(key="timestamp", freq=window)]
    )

    features = agg.agg(
        request_count=("endpoint", "count"),
        unique_endpoints=("endpoint", "nunique"),
        mean_time_diff=("time_diff", "mean"),
        std_time_diff=("time_diff", "std"),
        error_rate=("status", lambda x: np.mean(x >= 400)),
        rare_endpoint_ratio=("is_rare_endpoint", "mean"),
        avg_response_size=("size", "mean"),
        response_size_std=("size", "std")
    ).fillna(0)

    return features.reset_index()


if __name__ == "__main__":
    features = feature_engineering("data/processed_logs.csv")
    print(features.head())
    features.to_csv("data/engineered_features.csv", index=False)
  
"""

    # 1️⃣ Total number of feature rows
    print("Total feature rows:", len(features))

    # 2️⃣ Find suspicious behavior
    suspicious = features[
      (features["request_count"] > features["request_count"].quantile(0.95)) &
      (features["mean_time_diff"] < features["mean_time_diff"].quantile(0.05)) &
       (features["rare_endpoint_ratio"] > 0)
    ].sort_values("request_count", ascending=False)

    print("\n--- Suspicious example ---")
    print(suspicious.head(1))

    # 3️⃣ Find normal behavior
    normal = features[
        (features["request_count"] < features["request_count"].quantile(0.50)) &
        (features["error_rate"] < 0.1) &
       (features["rare_endpoint_ratio"] == 0)
    ]

    print("\n--- Normal example ---")
    print(normal.head(1))
"""