#!/usr/bin/env python

import os
import json
import requests
import re

akips_server = os.environ['AKIPS_HOST']
password = os.environ['AKIPS_PASS']
inventory = {'_meta': {'hostvars': {}}}

groupurl = 'https://{akips_server}/api-db?password={password};cmds=list+device+group'
groupresponse = requests.get(groupurl.format(akips_server=akips_server,
                                        password=password),
                        proxies={'http': None, 'https': None},
                        verify=os.path.dirname(os.path.realpath(__file__)) + "/cacert.cer")
grouplines = filter(None, groupresponse.text.split('\n'))

groupsuperurl = 'https://{akips_server}/api-db?password={password};cmds=list+device+super+group'
groupsuperresponse = requests.get(groupsuperurl.format(akips_server=akips_server,
                                        password=password),
                        proxies={'http': None, 'https': None},
                        verify=os.path.dirname(os.path.realpath(__file__)) + "/cacert.cer")
groupsuperlines = filter(None, groupsuperresponse.text.split('\n'))

groups = grouplines + groupsuperlines

for group in groups:
    # groups to ignore
    if group == 'maintenance_mode' or re.search(r'^4.*|AP$|Aruba|Linux|Servers$|^V-sl.*', group) or group == '':
        continue

    url = 'https://{akips_server}/api-db?password={password};cmds=mget+*+*+ping4+PING.icmpState+value+/up/+any+group+{group}'

    response = requests.get(url.format(akips_server=akips_server,
                                       password=password,
                                       group=group),
                            proxies={'http': None, 'https': None},
                            verify=os.path.dirname(os.path.realpath(__file__)) + "/cacert.cer")
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
        if re.search('IOS', group, re.IGNORECASE):
            inventory['_meta']['hostvars'][host].update({'ansible_network_os': 'ios'})
        if re.search('NX-OS', group, re.IGNORECASE):
            inventory['_meta']['hostvars'][host].update({'ansible_network_os': 'nxos'})

print json.dumps(inventory, indent=4, sort_keys=True)
