Discovery rule key: docker.image_names
Item prototypes key: docker.container.image_name[{#NAME}]
Trigger prototypes expression: last(/<template_name>/docker.container.image_name[{#NAME}])=0 
