import requests
import yaml
from datetime import datetime
from socket import gethostname
from pprint import pprint as pp

config = yaml.load(open('plumbing.yaml'))

headers = {'Access-Token': config['pushbullet']['access_token']}
payload = {
    'title': 'Test from Python',
    'body': 'This was sent at %s from %s' % (datetime.now(), gethostname()),
    'type': 'note',
}

print('Sending test notification via Pushbullet...')
r = requests.post('https://api.pushbullet.com/v2/pushes', headers=headers, json=payload)

print('Response code:', r.status_code)
