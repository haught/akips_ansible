#!/usr/bin/env python

import os
import json
import requests
import re

akips_server = os.environ['AKIPS_HOST']
password = os.environ['AKIPS_PASS']
exclude = r"\b(?=\w)" + os.environ['AKIPS_EXCLUDE'] + r"\b(?!\w)"

inventory = {'_meta': {'hostvars': {}}}

groupurl = 'https://{akips_server}/api-db?password={password};cmds=list+device+group'
groupresponse = requests.get(groupurl.format(akips_server=akips_server,
                                        password=password),
                        proxies={'http': None, 'https': None})
grouplines = filter(None, groupresponse.text.split('\n'))

groupsuperurl = 'https://{akips_server}/api-db?password={password};cmds=list+device+super+group'
groupsuperresponse = requests.get(groupsuperurl.format(akips_server=akips_server,
                                        password=password),
                        proxies={'http': None, 'https': None})
groupsuperlines = filter(None, groupsuperresponse.text.split('\n'))

groups = grouplines + groupsuperlines

for group in groups:
    # groups to ignore
    if group == '' or re.search(exclude, group):
        continue

    url = 'https://{akips_server}/api-db?password={password};cmds=mget+*+*+ping4+PING.icmpState+value+/up/+any+group+{group}'

    response = requests.get(url.format(akips_server=akips_server,
                                       password=password,
                                       group=group),
                            proxies={'http': None, 'https': None})
    lines = response.text.split('\n')
    inventory[group] = {'hosts': []}

    for line in lines:
        if line == '':
            continue
        host = line.split(' ')[0]
        ip = line.split(',')[-1]
        inventory[group]['hosts'].append(host)
        try:
            x = inventory['_meta']['hostvars'][host]
        except KeyError:
            inventory['_meta']['hostvars'][host] = {'ansible_host': ip}
        if re.search(os.environ['AKIPS_IOS_REGEX'] if 'AKIPS_IOS_REGEX' in os.environ else 'IOS', group, re.IGNORECASE):
            inventory['_meta']['hostvars'][host].update({'ansible_network_os': 'ios'})
        if re.search(os.environ['AKIPS_NXOS_REGEX'] if 'AKIPS_NXOS_REGEX' in os.environ else 'NX-OS', group, re.IGNORECASE):
            inventory['_meta']['hostvars'][host].update({'ansible_network_os': 'nxos'})
        if re.search(os.environ['AKIPS_ASA_REGEX'] if 'AKIPS_ASA_REGEX' in os.environ else 'ASA', group, re.IGNORECASE):
            inventory['_meta']['hostvars'][host].update({'ansible_network_os': 'asa'})

print(json.dumps(inventory, indent=4, sort_keys=True))
