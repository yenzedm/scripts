#Этот параметер добавить в агента забикса
UserParameter=docker.image_names,/path/to/image_names.py

#Этот параметер добавить в агента забикса
UserParameter=docker.container.image_name[*],/path/to/is_docker_container_available.py $1

#Этот ключ в discovery rule
docker.image_names

#Отслеживание докер контейнеров по имени образа
#Этот ключ в item
docker.container.image_name[{#NAME}]

#Expression для прототипа триггера
last(/hostname/docker.container.image_name[{#NAME}])=0
