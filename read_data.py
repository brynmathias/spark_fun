#!/usr/bin/env python
import plotly
import datetime
import simplejson
import requests

with open('./config.json') as config_file:
    plotly_user_config = simplejson.load(config_file)

username = plotly_user_config['plotly_username']
api_key = plotly_user_config['plotly_api_key']
stream_token = plotly_user_config['plotly_streaming_tokens'][0]
p = plotly.plotly(username, api_key)
p.plot([{'x': [], 'y': [], 'type': 'scatter', 'mode': 'lines',
         'stream': {'token': stream_token, 'maxpoints': 500}}],
       filename='Time-Series', fileopt='overwrite')
s = plotly.stream(stream_token)


while True:
    r = requests.get("https://api.spark.io/v1/devices/50ff70065067545638"
                     "200387/result?access_token="
                     "05970b102f05cd6f6cce1c5dcebccb096a222a63")
    x_data_point = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    a = simplejson.loads(r.text)
    y_data_point = simplejson.loads(a['result'])['data1']
    print x_data_point, y_data_point
    s.write({'x': x_data_point, 'y': y_data_point})
    print "written", x_data_point
