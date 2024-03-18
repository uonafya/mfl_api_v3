import requests
import base64

base_url = 'http://127.0.0.1:8000'
# base_url = 'https://api.kmhfltest.health.go.ke'

# client_id = '5O1KlpwBb96ANWe27ZQOpbWSF4DZDm4sOytwdzGv'
# client_secret = 'PqV0dHbkjXAtJYhY9UOCgRVi5BzLhiDxGU91kbt5EoayQ5SYOoJBYRYAYlJl2RetUeDMpSvhe9DaQr0HKHan0B9ptVyoLvOqpekiOmEqUJ6HZKuIoma0pvqkkKDU9GPv'

client_id = '1ArfkCfR9999VDGhbijKqUWHlSx9DX7EHJ77Ky4Z'
client_secret = 'DZFpuNjRdt5xUEzxXovAp40bU3lQvoMvF3awEStn61RXWE0Ses4RgzHWKJKTvUCHfRkhcBi3ebsEfSjfEO96vo2Sh6pZlxJ6f7KcUbhvqMMPoVxRwv4vfdWEoWMGPeIO'


credential = "{0}:{1}".format(client_id, client_secret)
tk = base64.b64encode(credential.encode("utf-8"))



headers = {"cache-control": "no-cache",
           "Content-Type": "application/x-www-form-urlencoded"}

# "Authorization": 'Basic %s' % tk

# red_url = 'http://127.0.0.1:8000/noexist/callback'

url = base_url + '/o/token/'
payload = {'grant_type': 'password', 'client_id': client_id,
           'client_secret': client_secret, 'username': 'nmugaya@gmail.com',
           'password': 'P@ss1234'}

response = requests.post(url, data=payload, headers=headers)
resp = response.json()

print(response.headers)
print(resp)


token = resp['access_token']
headers = {"Accept": "application/json", "Authorization": "Bearer %s" % token}


url = base_url + '/api/facilities/facilities/?format=json'
payload = {}

# response = requests.post(url, json=payload, headers=headers)
response = requests.get(url, params=payload, headers=headers)

# print(response.headers)
# print(response.text)
print(response.json())
