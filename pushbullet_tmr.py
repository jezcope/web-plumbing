import requests
import yaml
from pprint import pprint as pp

config = yaml.load(open('plumbing.yaml'))
tmr = config['tmr']

headers = {'Access-Token': config['pushbullet']['access_token']}
payload = {
    'push': {
        'type': 'messaging_extension_reply',
        'package_name': 'com.pushbullet.android',
        'conversation_iden': tmr['number'],
        'message': 'TMR %s %s %s' % (tmr['from'], tmr['to'], tmr['time']),
        'source_user_iden': 'USER_ID',
        'target_device_iden': 'DEVICE_ID',
    },
    'type': 'push',
}
pp(payload)

# r = requests.post('https://api.pushbullet.com/v2/ephemerals', headers=headers, json=payload)

# print('Response code:', r.status_code)
