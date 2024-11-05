import os
import requests
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv("APIKEY")
secretKey = os.getenv("SECRETKEY")
ruri = os.getenv("RURI")

rurl = urllib.parse.quote(ruri,safe="")

uri = f'https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={apiKey}&redirect_uri={rurl}'

print(uri) ## GET CODE FROM THE URL

code = ''

url = 'https://api.upstox.com/v2/login/authorization/token'

headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'code': code,
    'client_id': apiKey,
    'client_secret': secretKey,
    'redirect_uri': 'https://127.0.0.1:5000/',
    'grant_type': 'authorization_code'
}

response = requests.post(url, headers=headers, data=data)
response.json()

print(response)
print(response.json()['access_token'])