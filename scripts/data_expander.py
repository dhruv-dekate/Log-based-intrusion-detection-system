from datetime import timedelta
import random
import pandas as pd
from .log_parser import parse_log


def expand_logs(df, multiplier=200):
    """
    Expands log dataset by duplicating it multiple times
    and adding randomness to simulate realistic traffic.
    This is a simple way to create a larger dataset for training models without collecting more real data.
    """
    expanded = []

    for i in range(multiplier):
        temp = df.copy()
        # shift timestames by a few minutes to create variability
        temp["time"] = temp["time"] + timedelta(minutes=i)
        # randomize some columns
        temp["status"] = [random.choice([200, 404, 500]) for _ in range(len(temp))]
        temp["size"] = [random.randint(100, 5000) for _ in range(len(temp))]
        expanded.append(temp)
    big_df = pd.concat(expanded, ignore_index=True)
    return big_df

"""
if __name__ == "__main__":
    print("Parsing logs...")
    df = parse_log("data/access.log")
    print("Original rows:", len(df))
    expanded_df = expand_logs(df, multiplier=200)
    expanded_df.to_csv("data/processed_logs.csv", index=False)
    print("Expanded rows:", len(expanded_df))
    """