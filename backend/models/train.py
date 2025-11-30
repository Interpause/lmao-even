import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from setfit import SetFitModel, Trainer, TrainingArguments
from datasets import Dataset
from config import MODEL_PATH, LABEL2ID
from examples import FEW_SHOT_EXAMPLES


def train():
    dataset = Dataset.from_list(FEW_SHOT_EXAMPLES)
    dataset = dataset.map(lambda x: {"label": LABEL2ID[x["label"]]})

    model = SetFitModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    trainer = Trainer(
        model=model,
        args=TrainingArguments(batch_size=16, num_epochs=1),
        train_dataset=dataset,
    )

    trainer.train()
    model.save_pretrained(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()
