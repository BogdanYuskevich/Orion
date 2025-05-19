import requests

TOKEN = "7966266590:AAHJLrAQmL_-PrBmlWaHfHHJuxQ8ZlZXPHU"
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates")
print(response.json())