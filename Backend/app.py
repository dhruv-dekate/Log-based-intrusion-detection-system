from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from scripts.log_parser import parse_log
from scripts.feature_engineering import feature_engineering
from detection.fusion_score import fusion_detection

app = FastAPI()

# cors for react
app.add_middleware(
    CORSMiddleware,
    allow_origin=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/detect")
def detect():

    # step1 : parse log
    df = parse_log("data/access.log")
    df.to_csv("data/processed_log.csv", index=False)

    # Step 2: Feature engineering
    features = feature_engineering("data/processed_logs.csv")

    # Step 3: Detection
    results = fusion_detection(features)

    # -------------------------
    # Summary
    # -------------------------
    total = len(results)
    attack_count = int(results["fusion_flag"].sum())
    normal_count = total - attack_count
    attack_percent = (attack_count / total) * 100

    # -------------------------
    # Top suspicious IPs
    # -------------------------
    top_suspicious = results.sort_values(
        by="fusion_score", ascending=False
    ).head(5)[
        ["ip", "request_count", "error_rate", "fusion_score"]
    ].to_dict(orient="records")

    # -------------------------
    # Sample attacks
    # -------------------------
    sample_attacks = results[
        results["fusion_flag"] == 1
    ].head(5)[
        ["ip", "timestamp", "request_count", "fusion_score"]
    ].to_dict(orient="records")

    return {
        "total": total,
        "attacks": attack_count,
        "normal": normal_count,
        "attack_percent": attack_percent,
        "top_suspicious": top_suspicious,
        "sample_attacks": sample_attacks
    }