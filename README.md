# AKiPs AWX/Tower Inventory Source Script
This script will allow the use of AKiPs as a inventory source for AWX/Ansible Tower 
---

## Setup:



As an inventory source, use the akips_group.py script and set an AKiPs group as an environment variable
```
{
 "group": "0-Aruba-AP"
}
```
---
A new credential type will need to be created to store the information for AKiPs and the script.

*Name:*
```
AKiPs API
```

*Input Configuration:*
```yaml
---
fields:
  - id: hostname
    type: string
    label: Hostname
  - id: username
    type: string
    label: Username
  - id: password
    type: string
    label: Password
    secret: true
required:
  - hostname
  - password
```

*Injector Configuration:*
```yaml
---
env:
  AKIPS_HOST: '{{hostname}}'
  AKIPS_PASS: '{{password}}'
  AKIPS_USER: '{{username}}'
```

With the credential type added, the credentials will need to be added. Add a new credential and choose the new credential type you just created. Fill out the hostname, username, and password for your AKiPs API user (API must be enabled in AKiPs). 

With the credentials added, you will need to add your fork of this repostory as a new project just as you do for playbook projects.

Once the project is added you can create a new inventory and under the source add a new source as *Sourced from a Project* choosing your new credential, new project, and choose *akips.py* as your inventory file. Checking the *overwrite* box will remove devices no longer in AKiPs and is good to set.

For the environmental variables you can exclude specific AKiPs groups by setting the AKIPS_EXCLUDE variable. For example, if you wanted to exclude the *maintenance_mode*, *TrippLite*, and all groups ending in *AP* you could use:

```yaml
AKIPS_EXCLUDE: '^maintenance_mode$|TrippLite|AP$'
```

The inventory can now be synced. 