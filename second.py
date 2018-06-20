import requests
import json

username=""
password=""

payload={"username":username,"password":password}

adress="https://localhost:8443/api/s/default/stat/user/34:de:1a:22:35:8a"

page=requests.post(adress, data=payload)

data=json.loads(page.content)

print(data)