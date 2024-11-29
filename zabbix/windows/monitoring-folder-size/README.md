1. Type: zabbix agent
2. Item key: folder.size[C:/<name_folder>]
3. Trigger expression: last(/<template_name>/folder.size[C:/<name_folder>]) > 5000000000