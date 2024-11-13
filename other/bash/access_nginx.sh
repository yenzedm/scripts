#!/bin/bash

# path to conf
NGINX_CONF="$2"

CONTAINER_NAME="" # !!!

# check arg
if [ -z "$1" ]; then
    echo "inter 'on' or 'off' argument"
    exit 1
fi

if [ "$1" == "on" ]; then
    sed -i 's/#listen 23231;/listen 23231;/g' "$NGINX_CONF"
    sed -i 's/listen 127.0.0.1:23231;/#listen 127.0.0.1:23231;/g' "$NGINX_CONF"
    echo "nginx access on"
elif [ "$1" == "off" ]; then
    sed -i 's/listen 23231;/#listen 23231;/g' "$NGINX_CONF"
    sed -i 's/#listen 127.0.0.1:23231;/listen 127.0.0.1:23231;/g' "$NGINX_CONF"
    echo "nginx access off"
else
    echo "inter 'on' or 'off' argument"
    exit 1
fi

docker exec "$CONTAINER_NAME" nginx -s reload
if [ "$1" == "on" ]; then
    sleep 5
else
    :
fi

if curl --fail http://ip:port/; then   # !!!
    echo -e "\nrestart nginx done"    
else
    docker restart "$CONTAINER_NAME"
    echo "restart nginx done"
fi

exit 0
