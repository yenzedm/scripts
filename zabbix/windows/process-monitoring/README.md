1. Type: zabbix agent
2. Discovery rule key: service.names
3. Item prototypes key: service.name[{#NAME}]
4. Trigger prototypes expression: last(/<template_name>/service.name[{#NAME}])=0