Type: zabbix agent
Discovery rule key: service.names
Item prototypes key: service.name[{#NAME}]
Trigger prototypes expression: last(/<template_name>/service.name[{#NAME}])=0