#=======================
# rule base baseline
#=======================
from pyexpat import features
import pandas as pd
import numpy as np

def rule_base(row):
    score = 0

    
    if row['request_count'] > 60 :
     score += 2

    if row["unique_endpoints"] > 10:
      score += 2

    if row["mean_time_diff"] < 1:
       score += 2

    if row["error_rate"] > 0.3:
       score += 2

    if row["rare_endpoint_ratio"] > 0.05:
       score += 2

    return int(score)
"""
if __name__ == "__main__":
    df = pd.read_csv("data/engineered_features.csv")
    df["rule_base_score"] = df.apply(rule_base, axis=1)
    df["rule_base_flag"] = df["rule_base_score"].apply(lambda x: 1 if x >= 6 else 0)

    print(df[["request_count", "unique_endpoints", "mean_time_diff", "error_rate", "rare_endpoint_ratio", "rule_base_score", "rule_base_flag"]].head())
    print(df['rule_base_flag'].value_counts())
    print(df[df['rule_base_flag'] == 1].head())


    print(df.columns)"""