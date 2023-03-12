import requests
headers = {"User-Agent": "Comment Extraction"}
try:
    res = requests.get("https://www.nasdaq.com", timeout=1)
except Exception as e:
    print("error")