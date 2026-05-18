from requests import get

URL = "https://api.frankfurter.app/1995-01-01..2025-05-01"

params = {
    "from": "USD",
    "to": "EUR"
}

r = get(URL, params).json()

print(r)