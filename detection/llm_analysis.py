from ollama import chat

def analyze_attack(row):
    prompt = f"""
    you are a cybersecurity expert. Analyze  this web traffic behaviour.

    IP : {row['ip']}
    Request Count: {row['request_count']}
    Unique Endpoints: {row['unique_endpoints']}
    Error Rate: {row['error_rate']}
    Rare Endpoint Ratio: {row['rare_endpoint_ratio']}
    Fusion Score: {row['fusion_score']}

    Explain :
    Explain what a cyber attack and why, in one sentence
    """

    response = chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']