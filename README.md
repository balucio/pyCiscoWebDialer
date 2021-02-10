# pyCiscoWebDialer
Use Cisco CallManager WebDialer API to Make a PhoneCall.

How to use:

First of all you need to **Change Cisco Call Manager (WebDialer) Ip address** at line 12 in code.

```bash
   usage: ciscoDial.py [-h] --username USERNAME --password PASSWORD
                    [--profile PROFILE] --callto CALLTO
```

Example:

For proxied call you need to specify the proxy user and also the caller profile (telephone number):

```bash
 ./ciscoDial.py  --username=8140 --password=8140 --profile=8140 --callto=8139
```

For non proxied user the profile can be omitted, in this case user value will be used:

```bash
 ./ciscoDial.py  --username=8140 --password=8140  --callto=8139 
```
