import pandas as pd
from .isolation_forest import detect_anomalies
from .rule_base import rule_base


def fusion_detection(df):

    # rule based score
    df["rule_score"] = df.apply(rule_base, axis=1)

    # rule flag
    df["rule_flag"] = df["rule_score"].apply(lambda x: 1 if x >= 6 else 0)

    # ML anomaly detection
    anomalies = detect_anomalies(df)

    df["ml_flag"] = anomalies.map({1: 0, -1: 1})

    # Fusion score
    df["fusion_score"] = df["rule_score"] + (df["ml_flag"] * 3)

    # Final decision
    df["fusion_flag"] = df["fusion_score"].apply(lambda x: 1 if x >= 6 else 0)

    return df


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