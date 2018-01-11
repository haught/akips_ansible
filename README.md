# akips_ansible
Akips ansible inventory script
---
As an inventory source, use the akips_group.py script and set an AKiPs group as an environment variable
```
{
 "group": "0-Aruba-AP"
}
```
---
The credential store holds AKiPs host and username/password.

A new credential type needs to be created with the following:

*Input Configuration:*
```
fields:
  - type: string
    id: hostname
    label: Hostname
  - type: string
    id: username
    label: Username
  - secret: true
    type: string
    id: password
    label: Password
required:
  - hostname
  - password
```

*Injector Configuration:*
```
env:
  AKIPS_HOST: '{{hostname}}'
  AKIPS_PASS: '{{password}}'
  AKIPS_USER: '{{username}}'
```
