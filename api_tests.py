import requests
import base64

import random
import string
import hashlib

base_url = 'http://127.0.0.1:8000'
# base_url = 'https://api.kmhfltest.health.go.ke'

# client_id = '5O1KlpwBb96ANWe27ZQOpbWSF4DZDm4sOytwdzGv'
# client_secret = 'PqV0dHbkjXAtJYhY9UOCgRVi5BzLhiDxGU91kbt5EoayQ5SYOoJBYRYAYlJl2RetUeDMpSvhe9DaQr0HKHan0B9ptVyoLvOqpekiOmEqUJ6HZKuIoma0pvqkkKDU9GPv'

# client_id = '1ArfkCfR9999VDGhbijKqUWHlSx9DX7EHJ77Ky4Z'
client_id = '1ArfkCfR9999VDGhbijKqUWHlSx9DX7EHJ77Ky4Z'
# client_secret = 'pbkdf2_sha256$600000$jP40ti2i2obcmSROOyp2Ir$Caj4MFEgo72nXczWqWRMF40AX+cLqlHL9HKRqIw4x+Q='
client_secret = 'DZFpuNjRdt5xUEzxXovAp40bU3lQvoMvF3awEStn61RXWE0Ses4RgzHWKJKTvUCHfRkhcBi3ebsEfSjfEO96vo2Sh6pZlxJ6f7KcUbhvqMMPoVxRwv4vfdWEoWMGPeIO'

tkb = ('%s:%s' % (client_id, client_secret)).encode("ascii")
tk = base64.b64encode(tkb)

headers = {"Accept": "application/json",
           "cache-control": "no-cache",
           "Content-Type": "application/x-www-form-urlencoded"}

# "Authorization": 'Basic %s' % tk

red_url = 'http://127.0.0.1:8000/noexist/callback'
'''
code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))

code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

print('CV', code_verifier)
print('CC', code_challenge)
# cv - AN1IJT9KC54CD2AU06MBCUCSQ6BIF3LJJBYLWOCZA5EHMMQSO5HJL2MBF7MHFMJN92CHV1J7MB43WOEPYJ1IFUXAHS3WOGRCFMDVBL5BO5U8QJOYX8DMQ5S
# cc - zZDODPG_s9FPtqmth2pIsl0z5euORTWbEwKRTxqcm0M

a_url = base_url + '/o/authorize/'
params = {'response_type' : 'code', 'code_challenge': code_challenge,
          'code_challenge_method': 'S256', 'client_id': client_id,
          'redirect_uri': 'http://127.0.0.1:8000/noexist/callback'}

code = '%s?response_type=code&code_challenge=%s&code_challenge_method=S256&client_id=%s&redirect_uri=%s' % (a_url, code_challenge, client_id, red_url)
print(code)
'''

code_verifier = 'AN1IJT9KC54CD2AU06MBCUCSQ6BIF3LJJBYLWOCZA5EHMMQSO5HJL2MBF7MHFMJN92CHV1J7MB43WOEPYJ1IFUXAHS3WOGRCFMDVBL5BO5U8QJOYX8DMQ5S'
code = '87kKTI7534sfsvoL4sUmfVaLcVOXxj'

url = base_url + '/o/token/'
payload = {'username': 'nmugaya@gmail.com', 'password': 'P@ss1234', 'grant_type': 'authorization_code',
           'client_id': client_id, 'client_secret': client_secret,
           'code': code, 'code_verifier': code_verifier, 'redirect_uri': red_url}

'''
payload = {'username': 'erotush77@gmail.com', 'password': 'emutuaMFL@77', 'grant_type': 'password',
           'scope': 'read', 'client_id': client_id, 'client_secret': client_secret}
'''
headers = {"Cache-Control": "no-cache",
           "Content-Type": "application/x-www-form-urlencoded"}
# response = requests.post(url, params=payload, headers=headers)
response = requests.post(url, data=payload, headers=headers)
resp = response.json()

print(response.headers)
print(resp)

token = resp['access_token']
headers = {"Accept": "application/json", "Authorization": "Bearer %s" % token}


url = base_url + '/api/facilities/facilities/'
payload = {}

# response = requests.post(url, json=payload, headers=headers)
response = requests.get(url, params=payload, headers=headers)

# print(response.headers)
# print(response.text)
print(response.json())
