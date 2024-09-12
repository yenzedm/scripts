#!/usr/bin/python3
import os
import json


def json_image_name():
    image_name_list = []
    image_name_json = []

    with os.popen("docker images --format {{.Repository}}:{{.Tag}}") as file:
        for image_name in file:
            if image_name.strip() in image_name_list:
                continue
            if '<none>' in image_name.strip():
                image_name_list.append(''.join(image_name.split(':')[:-1]).strip())
            else:
                image_name_list.append(image_name.strip())

    for image_name in image_name_list:
        image_name_json.append({'{#NAME}': image_name})

    image_name_json = json.dumps(image_name_json)
    print(image_name_json)
    return image_name_json


if __name__ == '__main__':
    json_image_name()
