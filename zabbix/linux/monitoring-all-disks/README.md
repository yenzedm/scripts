###### without scripts 

1. Type: zabbix-agent
2. Item prototypes key: vfs.fs.size[/,free]
3. Trigger prototypes expression: last(/<template_name or host>/vfs.fs.size[/,free]) \< \<number of bytes\> 25000000000 = 25gb