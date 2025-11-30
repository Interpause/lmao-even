from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import torch
from setfit import SetFitModel
from config import MODEL_PATH, DATA_DIR, ACTIONABLE_BUCKETS, ID2LABEL
from pipeline import classify, generate_response
import os

# Global state
model = None
messages_df = None


def get_device():
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    return "cpu"


def df_to_json_safe(df: pd.DataFrame) -> list[dict]:
    """Convert DataFrame to JSON-safe list of dicts, handling NaN values."""
    return df.fillna("").to_dict(orient="records")


def generate_responses_batched(df: pd.DataFrame, batch_size: int = 5) -> list[str]:
    """Generate responses for actionable messages in batches."""
    from pipeline import generate_response as gen_response

    responses = []
    total = len(df)

    for i in range(0, total, batch_size):
        batch = df.iloc[i:i+batch_size]
        print(f"Generating responses {i+1}-{min(i+batch_size, total)} of {total}...")
        for _, row in batch.iterrows():
            responses.append(gen_response(row))

    return responses


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, messages_df

    device = get_device()
    print(f"Loading model on {device}...")
    model = SetFitModel.from_pretrained(MODEL_PATH)
    model.to(device)

    print("Loading and classifying messages...")
    messages_df = pd.read_csv(os.path.join(DATA_DIR, "your_messages.csv"))
    messages_df = classify(messages_df, model)
    print(f"Loaded {len(messages_df)} messages")

    # Pre-generate responses for actionable messages
    actionable_mask = messages_df["action_bucket"].isin(ACTIONABLE_BUCKETS)
    actionable_df = messages_df[actionable_mask]

    if len(actionable_df) > 0:
        print(f"Pre-generating responses for {len(actionable_df)} actionable messages...")
        messages_df.loc[actionable_mask, "draft_response"] = generate_responses_batched(actionable_df)
    else:
        messages_df["draft_response"] = ""

    # Fill non-actionable with empty string
    messages_df["draft_response"] = messages_df["draft_response"].fillna("")

    print("Startup complete.")
    yield


app = FastAPI(title="Message Classification API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/tags")
async def get_tags():
    """List available classification tags."""
    return {
        "tags": list(ID2LABEL.values()),
        "actionable": ACTIONABLE_BUCKETS
    }


@app.get("/messages")
async def get_messages():
    """Get all messages grouped by tag."""
    if messages_df is None:
        raise HTTPException(status_code=503, detail="Messages not loaded")

    grouped = {}
    for tag in ID2LABEL.values():
        tag_messages = messages_df[messages_df["action_bucket"] == tag]
        grouped[tag] = df_to_json_safe(tag_messages)

    return grouped


@app.get("/messages/{tag}")
async def get_messages_by_tag(tag: str):
    """Get messages for a specific tag."""
    if messages_df is None:
        raise HTTPException(status_code=503, detail="Messages not loaded")

    if tag not in ID2LABEL.values():
        raise HTTPException(status_code=404, detail=f"Unknown tag: {tag}")

    tag_messages = messages_df[messages_df["action_bucket"] == tag]
    return {
        "tag": tag,
        "count": len(tag_messages),
        "messages": df_to_json_safe(tag_messages)
    }


@app.post("/generate-response/{message_id}")
async def generate_response_for_message(message_id: str):
    """Generate a draft response for an actionable message."""
    if messages_df is None:
        raise HTTPException(status_code=503, detail="Messages not loaded")

    row = messages_df[messages_df["message_id"] == message_id]
    if row.empty:
        raise HTTPException(status_code=404, detail=f"Message not found: {message_id}")

    row = row.iloc[0]

    if row["action_bucket"] not in ACTIONABLE_BUCKETS:
        raise HTTPException(
            status_code=400,
            detail=f"Message is not actionable (tag: {row['action_bucket']})"
        )

    draft = generate_response(row)

    return {
        "message_id": message_id,
        "tag": row["action_bucket"],
        "draft_response": draft
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
