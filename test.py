test = [
    {
        "ticker": "TSLA",
        "new": False
    },
    {
        "ticker": "APPL",
        "new": True
    },
    {
        "ticker": "SPY",
        "new": False
    }
]

print("KK" in [d["ticker"] for d in test])