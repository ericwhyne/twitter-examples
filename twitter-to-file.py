#!/usr/bin/env python
import os
import yaml
import json
from birdy.twitter import StreamClient
import sys

keywordsfile = sys.argv[1]
with open(keywordsfile) as f:
    keywords = f.read().splitlines()
keywords_string = ','.join(set(keywords))

tokenfile = os.path.expanduser("~") + "/.twitterapi/phil.yml"
tokens = yaml.safe_load(open(tokenfile))

client = StreamClient(tokens['consumer_key'],tokens['consumer_secret'],tokens['access_token'],tokens['access_secret'])
resource = client.stream.statuses.filter.post(track=keywords_string)

for data in resource.stream():
  tweet = json.dumps(data) + '\n'
  if 'text' in data:
    print data['text']
