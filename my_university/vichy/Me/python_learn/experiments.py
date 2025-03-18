import requests

res = requests.get(
    "https://upload.wikimedia.org/wikipedia/ru/a/af/Valve_Deadlock_icon.png"
)
with open("deadlock.png", "wb") as f:
    f.write(res.content)
