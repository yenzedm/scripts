1. permissions /etc/sudoers: zabbix  ALL=(ALL) NOPASSWD: /usr/bin/du
2. Type: zabbix agent
3. Item key: folder.size[<path/to/target>]
4. Trigger expression: last(/<template_name or host>/folder.size[<path/to/target>]) > 5000000000
