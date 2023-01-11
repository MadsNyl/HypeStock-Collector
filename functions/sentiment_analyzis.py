from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np

def analyze(text: str) -> dict[str: float]:
    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    encoded_text = tokenizer(text, return_tensors="pt")
    results = model(**encoded_text)
    results = results[0][0].detach().numpy()
    results = softmax(results)
    roberta = {
        "neg": convert_to_float(results[0]),
        "neu": convert_to_float(results[1]),
        "pos": convert_to_float(results[2])
    }

    return roberta

def convert_to_float(np_float) -> float: return np.float32(np_float).item()