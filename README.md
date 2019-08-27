# AKiPs AWX/Tower Inventory Source

This script will allow the use of AKiPs as a inventory source for AWX/Ansible Tower.

## Setup:

A new credential type will need to be created to store the information for your AKiPs API user.

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

With the credential type added, the actual credentials will need to be added. Add a new credential and choose the new credential type you just created. Fill out the hostname, username (not actually used), and password for your AKiPs API user (API must be enabled in AKiPs).

With the credentials added, you will need to add your fork of this repostory as a new project just as you do for playbook projects.

Once the project is added and synced you can create a new inventory and under *Source* add a new one as *Sourced from a Project* choosing your new credential you just added, new project you just added, and choose *akips.py* as your inventory file. Checking the *overwrite* box will remove devices no longer in AKiPs and is good to set if there is only one source.

For the environmental variables you can exclude specific AKiPs groups by setting the AKIPS_EXCLUDE_GROUPS and AKIPS_EXCLUDE_HOSTS variables. For example, if you wanted to exclude the *maintenance_mode* group, *TrippLite* group, and all groups ending in *AP* you could use:

```yaml
AKIPS_EXCLUDE_GROUPS: >-
  ^maintenance_mode$|TrippLite|AP$
```

If you needed to exclude hosts starting with *lab*, you could use:

```yaml
AKIPS_EXCLUDE_HOSTS: >-
  ^lab
```

There are also variables for *AKIPS_IOS_REGEX*, *AKIPS_NXOS_REGEX*, and *AKIPS_ASA_REGEX* that will overwrite the default ones in the script to adding *ansible_network_os* values to the hosts.

## Fin:

The inventory can now be synced. You can use your AKiPs groups for the *limit* value for your playbook templates. Setting a scheduled run for the source will keep things up to date automatically.