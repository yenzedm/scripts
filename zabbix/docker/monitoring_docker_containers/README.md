1. Discovery rule key: docker.image_names
2. Item prototypes key: docker.container.image_name[{#NAME}]
3. Trigger prototypes expression: last(/<template_name>/docker.container.image_name[{#NAME}])=0 
