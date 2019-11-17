# Mongo cluster automation
* This tool can help you create a cluster of three instance with some types
## Requires:
* There shared folder of three instance MongoDB, they named on config/config.json file.
## Steps
* On master node: 
<code> ./main.py master init </code>
<code> ./main.py master create </code>
* On slave node 0:
<code> ./main.py slave 0 start </code>
* On slave node 1:
<code> ./main.py slave 1 start </code>
* On master node:
<code> ./main.py master add </code>
## About
