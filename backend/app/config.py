import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "message_classifier_model")
DATA_DIR = os.path.join(BASE_DIR, "data")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_HOST}/api/chat"
OLLAMA_MODEL = "gpt-oss:20b"
ACTIONABLE_BUCKETS = ["requires_response", "requires_decision"]

ID2LABEL = {
    0: "requires_response",
    1: "requires_decision", 
    2: "requires_review",
    3: "financial_action",
    4: "alert",
    5: "notification",
    6: "personal"
}

LABEL2ID = {v: k for k, v in ID2LABEL.items()}