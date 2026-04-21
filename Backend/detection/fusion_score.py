import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from .isolation_forest import detect_anomalies
from .rule_base import rule_base


def fusion_detection(df):

    # rule based score
    df["rule_score"] = df.apply(rule_base, axis=1)
   
    # rule flag
    df["rule_flag"] = df["rule_score"].apply(lambda x: 1 if x >= 6 else 0)

    # ML anomaly detection

    anomalies = detect_anomalies(df)

    df["ml_flag"] = anomalies["anomaly_label"].map({1: 0, -1: 1})
    df["ml_score"] = anomalies["anomaly_score"]

    # Normalize
    scaler = MinMaxScaler()
    df["rule_norm"] = scaler.fit_transform(df[["rule_score"]])
    df["ml_norm"] = scaler.fit_transform(df[["ml_score"]])

    # Fusion
    df["fusion_score"] = df["rule_norm"] + df["ml_norm"]

    # Adaptive threshold
    threshold = df["fusion_score"].quantile(0.95)

    df["fusion_flag"] = (df["fusion_score"] >= threshold).astype(int)

    return df

def explain_attack(row):
    reasons = []

    if row["request_count"] > 50:
        reasons.append("High request volume")

    if row["error_rate"] > 0.3:
        reasons.append("High error rate")

    if row["rare_endpoint_ratio"] > 0.05:
        reasons.append("Accessing rare endpoints")

    if row["ml_flag"] == 1:
        reasons.append("Anomalous pattern detected (ML)")

    return ", ".join(reasons)

if __name__ == "__main__":

    df = pd.read_csv("data/engineered_features.csv")

    results = fusion_detection(df)

    print(results[[
        "request_count",
        "unique_endpoints",
        "error_rate",
        "rule_score",
        "rule_flag",
        "ml_flag",
        "fusion_score",
        "fusion_flag"
    ]].head())

    print("\nFusion detections:")
    print(results["fusion_flag"].value_counts())

    results.to_csv("data/fusion_results.csv", index=False)