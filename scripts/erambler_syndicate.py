import feedparser
from datetime import datetime as dt
from time import mktime
import yaml
import requests

class BufferSyndicate:
    def __init__(self, config, now=False, format_string='Recently blogged: {title}'):
        self.config = config['buffer']
        self.now = now
        self.format_string = format_string

    def syndicate(self, title, teaser, url):
        text = self.format_string.format(title=title, teaser=teaser)

        print('Sending to buffer: "{} {}"... '.format(text, url), end='\n', flush=True)

        r = requests.post('https://api.bufferapp.com/1/updates/create.json',
                          data={
                              'access_token': self.config['access_token'],
                              'profile_ids[]': [self.config['tw_profile']],
                              'text': text,
                              'media[link]': url,
                              'now': str(self.now).lower()
                              })

        if r.status_code == 200:
            print('Success')
        else:
            print('Failed with code {}'.format(r.status_code))
            print('Error:', r.json()['message'])

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

syndicate = [BufferSyndicate(config),
             BufferSyndicate(config, now=True, format_string='{teaser}')]

last_updated = state.get('er_last_updated', dt(2000, 1, 2))

for entry in feed.entries:
    entry_updated = dt.fromtimestamp(mktime(entry.updated_parsed))
    if entry_updated > last_updated:
        for s in syndicate:
            s.syndicate(title=entry.title,
                        teaser=entry.get('prism_teaser', entry.title),
                        url=entry.link)

state['er_last_updated'] = dt.fromtimestamp(mktime(feed.updated_parsed))
yaml.dump(state, open('plumbing-state.yaml', 'w'), default_flow_style=False)
