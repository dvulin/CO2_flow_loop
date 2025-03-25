import requests
import datetime

#url = "http://127.0.0.1:8000/calculate"
url = "https://test-production-f873.up.railway.app/calculate"

begin = datetime.datetime.now()

input_data = {
    "nsteps": 40,
    "length": 40000 
}

response = requests.post(url, json=input_data)

if response.status_code == 200:
    result = response.json()
    end = datetime.datetime.now()
    runtime = end - begin
    print(f"p2: {result}  in {runtime} seconds")
else:
    print(f"Greska: {response.status_code}, {response.text}")