import requests

url = "http://localhost:5000/"
res = requests.get(url)
print(res.text)

