import feedparser
from datetime import datetime as dt
from time import mktime
import yaml
import requests

class BufferSyndicate:
    def __init__(self, config):
        self.config = config['buffer']

    def syndicate(self, text, url):
        print('Sending to buffer: "{} {}"... '.format(text, url), end='', flush=True)

        r = requests.post('https://api.bufferapp.com/1/updates/create.json',
                          data={
                              'access_token': self.config['access_token'],
                              'profile_ids[]': [self.config['tw_profile'],
                                                self.config['fb_profile']],
                              'text': text,
                              'media[link]': url
                              })

        if r.status_code == 200:
            print('Success')
        else:
            print('Failed with code {}'.format(r.status_code))
            print('Error:', r.json()['message'])

class TweetNowSyndicate:
    pass

class EmailNotifySyndicate:
    pass

feed = feedparser.parse('http://erambler.co.uk/feed.xml')

try:
    with open('plumbing-state.yaml') as f:
        state = yaml.load(f)
except:
    state = {}

with open('plumbing.yaml') as f:
    config = yaml.load(f)

syndicate = [BufferSyndicate(config)]

last_updated = state.get('er_last_updated', dt(2000, 1, 2))

for entry in feed.entries:
    entry_updated = dt.fromtimestamp(mktime(entry.updated_parsed))
    if entry_updated > last_updated:
        for s in syndicate:
            s.syndicate('Recently blogged: ' + entry.title, entry.link)

state['er_last_updated'] = dt.now()
yaml.dump(state, open('plumbing-state.yaml', 'w'), default_flow_style=False)
