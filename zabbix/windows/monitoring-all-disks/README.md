###### without scripts 

1. Type: zabbix-agent
2. Discovery rule key: vfs.fs.discovery
3. Item prototypes key: vfs.fs.size[{#FSNAME},free]
4. Trigger prototypes expression: last(/<template_name or host>/vfs.fs.size[{#FSNAME},free])<25000000000