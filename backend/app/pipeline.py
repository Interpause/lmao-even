import pandas as pd
import requests
import torch
from setfit import SetFitModel
from config import MODEL_PATH, OLLAMA_URL, OLLAMA_MODEL, ACTIONABLE_BUCKETS, ID2LABEL


def get_device():
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    return "cpu"


def classify(df: pd.DataFrame, model: SetFitModel) -> pd.DataFrame:
    df["text_for_classification"] = df["subject_or_topic"] + ": " + df["message_snippet"]
    
    predictions = model.predict(df["text_for_classification"].tolist())
    probabilities = model.predict_proba(df["text_for_classification"].tolist())
    
    df["action_bucket"] = [ID2LABEL[int(p)] for p in predictions]
    df["classification_confidence"] = [float(max(prob)) for prob in probabilities]
    df = df.drop(columns=["text_for_classification"])
    
    return df


def extract_actionable(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["action_bucket"].isin(ACTIONABLE_BUCKETS)].copy()


def generate_response(row: pd.Series) -> str:
    prompt = f"""You are an assistant helping a small business owner (AuroraSkin, a skincare brand) draft responses.

Message details:
- From: {row['sender_name']} ({row['sender_handle_or_email']})
- Subject: {row['subject_or_topic']}
- Message: {row['message_snippet']}
- Source: {row['source_system']} / {row['channel_name']}
- Category: {row['category']}
- Order ID: {row.get('order_id', 'N/A')}

Draft a brief, professional response. Be helpful and on-brand for a skincare company. Keep it concise."""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
    )
    
    data = response.json()
    
    # Debug: print if error
    if "message" not in data:
        print(f"Ollama error: {data}")
        return f"ERROR: {data.get('error', 'Unknown error')}"
    
    return data["message"]["content"]


def process_actionable_messages(df: pd.DataFrame) -> pd.DataFrame:
    responses = []
    for _, row in df.iterrows():
        print(f"Generating response for {row['message_id']}...")
        responses.append(generate_response(row))
    
    df["draft_response"] = responses
    return df


def main(input_csv: str):
    device = get_device()
    print(f"Using device: {device}")
    
    print("Loading classifier...")
    model = SetFitModel.from_pretrained(MODEL_PATH)
    model.to(device)
    
    print("Classifying messages...")
    df = pd.read_csv(input_csv)
    df = classify(df, model)
    df.to_csv("processed_messages.csv", index=False)
    
    actionable = extract_actionable(df)
    print(f"\nFound {len(actionable)} actionable messages")
    
    print("\nGenerating draft responses...")
    actionable = process_actionable_messages(actionable)
    actionable.to_csv("actionable_with_drafts.csv", index=False)
    
    print("\nDone.")


if __name__ == "__main__":
    main("your_messages.csv")