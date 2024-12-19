###### without scripts

1. Type: zabbix-agent
2. Item prototypes key: cpu.total
3. Trigger prototypes expression: last(/<template_name or host>/cpu.total) \> \<number of percent\>