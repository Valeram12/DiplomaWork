import base64
import requests
import json

APP_KEY = ''
APP_SECRET = ''
REFRESH_TOKEN = ''


ACCESS_CODE_GENERATED = ''

BASIC_AUTH = base64.b64encode(f'{APP_KEY}:{APP_SECRET}'.encode())

headers = {
    'Authorization': f"Basic {BASIC_AUTH}",
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = f'code={ACCESS_CODE_GENERATED}&grant_type=authorization_code'

response = requests.post('https://api.dropboxapi.com/oauth2/token',
                         data=data,
                         auth=(APP_KEY, APP_SECRET))
print(json.dumps(json.loads(response.text), indent=2))


def get_access_token(refresh_token, app_key, app_secret):
    url = 'https://api.dropboxapi.com/oauth2/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': app_key,
        'client_secret': app_secret
    }
    response = requests.post(url, data=data)
    response_data = response.json()
    access_token = response_data.get('access_token')
    print(response_data)
    return response_data


str(get_access_token(REFRESH_TOKEN, APP_KEY, APP_SECRET))
