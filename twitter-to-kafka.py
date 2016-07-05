#!/usr/bin/python
import os
import yaml
import json
from birdy.twitter import StreamClient
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
import sys

keywordsfile = sys.argv[1]
tokenfile = os.path.expanduser("~") + "/.twitterapi/tokenfile-example.yml"
kafkanodes = 'xd-kafka01:9092, xd-kafka02:9092, xd-kafka03:9092, xd-kafka04:9092'

with open(keywordsfile) as f:
    keywords = f.read().splitlines()
keywords_string = ','.join(set(keywords))

client = KafkaClient(kafkanodes)
producer = SimpleProducer(client)

tokens = yaml.safe_load(open(tokenfile))
client = StreamClient(tokens['consumer_key'],tokens['consumer_secret'],tokens['access_token'],tokens['access_secret'])
resource = client.stream.statuses.filter.post(track=keywords_string)

for data in resource.stream():
  tweet = json.dumps(data) + '\n'
  if 'text' in data:
    print data['text']
  producer.send_messages('twitter', tweet)
