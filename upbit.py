import os
import jwt
import uuid
import hashlib
import json
from urllib.parse import urlencode

import requests

access_key = 'QexQ17ASnvWFrfFi5qrYFVHiPbWkXdhPssNDsOI1'
secret_key = 'pENH1O2ptxTUG5ivK6QkLkjvnHPOYfkXrOTN3fzx'
server_url = 'https://api.upbit.com'

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/accounts", headers=headers)

print(res.json())