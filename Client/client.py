#!/usr/bin/env python3
# coding:utf8

import urllib.parse
import urllib.request


url = 'http://127.0.0.1:12345'
data = {
    'hostname': 'find-pc',
    'ip': '123.2.1.2',
    'comment': 'mainPC',
    'password': 'pass'
}

postData = urllib.parse.urlencode(data).encode('utf8')
req = urllib.request.Request(url, postData)
req.add_header('Referer', 'http://www.python.org/')
response = urllib.request.urlopen(req)
print(response.read().decode('utf8'))