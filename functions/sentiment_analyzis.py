from nltk.sentiment import SentimentIntensityAnalyzer

def analyze(text: str) -> float:
    sia = SentimentIntensityAnalyzer()
    results = sia.polarity_scores(text)
    return results["compound"]