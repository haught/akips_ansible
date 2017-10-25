#!/usr/bin/env python

import os
import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


akips_server = os.environ['server']
password = os.environ['pass']
groups = [
          '9-AFH-Lab',
          'CS-Servers',
         ]
group_list = '+'.join(groups)

proxies = {
            'http': None,
            'https': None,
}

url = 'https://{akips_server}/api-db?password={password};cmds=mget+*+*+ping4+PING.icmpState+value+/up/+any+group+{group_list}'
response = requests.get(url.format(akips_server=akips_server,
                                   password=password,
                                   group_list=group_list),
                        proxies=proxies,
                        verify=False)
lines = response.text.split('\n')
inventory = {
#             'ios': {'hosts': []},
             '_meta': {'hostvars': {}},
            }

for line in lines:
    if line == '':
        continue
    host, _, _, _, data= line.split(' ')
    ip = data.split(',')[-1]
#    inventory['ios']['hosts'].append(host)
    inventory['_meta']['hostvars'][host] = {'ansible_host': ip}

print json.dumps(inventory)

