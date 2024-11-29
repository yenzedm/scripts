without scripts 

Type: zabbix-agent
Discovery rule key: vfs.fs.discovery
Item prototypes key: vfs.fs.size[{#FSNAME},free]
Trigger prototypes expression: last(/10.7.54.155/vfs.fs.size[{#FSNAME},free])<25000000000