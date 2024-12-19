1. Type: zabbix agent
2. Item key: folder.size[C:/<name_folder>]
3. Trigger expression: last(/<template_name or host>/folder.size[C:/<name_folder>]) \> \<number of bytes\> 25000000000 = 25gb