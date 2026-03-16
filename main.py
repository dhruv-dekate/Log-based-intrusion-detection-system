from scripts.log_parser import parse_log
from scripts.data_expander import expand_logs
from scripts.feature_engineering import feature_engineering
from detection.fusion_score import fusion_detection
from detection.llm_analysis import analyze_attack

import pandas as pd


def main(use_expander=False):

    print("========== LOG IDS PIPELINE ==========")

    # -----------------------------
    #  Parse raw logs
    # -----------------------------
    print("\n[1] Parsing raw logs...")
    df = parse_log("data/access.log")
    print("Parsed rows:", len(df))

    # -----------------------------
    # Optional data expansion
    # -----------------------------
    if use_expander:
        print("\n[2] Expanding dataset...")
        df = expand_logs(df, multiplier=200)
        print("Expanded rows:", len(df))

    # Save processed logs
    df.to_csv("data/processed_logs.csv", index=False)

    # -----------------------------
    # Feature engineering
    # -----------------------------
    print("\n[3] Creating features...")
    features = feature_engineering("data/processed_logs.csv")
    features.to_csv("data/engineered_features.csv", index=False)
    print("Feature rows:", len(features))

    # -----------------------------
    # Fusion detection
    # -----------------------------
    print("\n[4] Running hybrid IDS (Rule + ML)...")

    features = pd.read_csv("data/engineered_features.csv")
    results = fusion_detection(features)

    # -----------------------------
    # Summary
    # -----------------------------

    print("\n========== RESULTS SUMMARY ==========")

    print("Total records:", len(results))

    print("\nDetected attacks:")
    print(f'total: {results["fusion_flag"].sum()}')
    print(results["fusion_flag"].value_counts())


    total = len(results)

    attack_count = results["fusion_flag"].sum()
    normal_count = total - attack_count

    attack_percent = (attack_count / total) * 100
    normal_percent = (normal_count / total) * 100

    print(f"\nTotal records analysed: {total}")

    print(f"\nNormal traffic : {normal_count} ({normal_percent:.2f}%)")
    print(f"Detected attacks: {attack_count} ({attack_percent:.2f}%)")
    print("\nSample detected attacks:")
    print(f'few of detected attacks : {results[results["fusion_flag"] == 1].head(5)}')

# -----------------------------
# Additional useful statistics
# -----------------------------

    print("\n--- Traffic Behavior Stats ---")

    print("Average request count:", round(results["request_count"].mean(), 2))
    print("Max request count:", results["request_count"].max())

    print("Average error rate:", round(results["error_rate"].mean(), 3))

    print("Average rare endpoint ratio:",
    round(results["rare_endpoint_ratio"].mean(), 3))


# -----------------------------
# Top suspicious IP activity
# -----------------------------

    print("\n--- Most Suspicious Activity ---")

    top_suspicious = results.sort_values(
       by="fusion_score", ascending=False
    ).head(5)

    print(top_suspicious[
        ["ip",
         "request_count",
         "unique_endpoints",
         "error_rate",
         "fusion_score"]
    ])
    
    #================================
    # LLM analysis of detected attacks
    #================================

    attacks = results[results["fusion_flag"] == 1]

    for i, row in attacks.head(5).iterrows():

        explanation = analyze_attack(row)

        print("\n=========================")
        print("Attack IP:", row["ip"])
        print("Fusion Score:", row["fusion_score"])
        print("\nLLM Analysis:")
        print(explanation)


if __name__ == "__main__":

    # Set use_expander=True to create a larger dataset for testing
    
    main(use_expander=False)
