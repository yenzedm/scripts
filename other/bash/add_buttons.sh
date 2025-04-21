#!/bin/bash

input_file="template.html"
output_file="index.html"
buttons_file="buttons.txt"

# Собираем кнопки из файла
buttons=""
while IFS="|" read -r path name; do
  buttons+="    <button onclick=\"loadPage('$path')\">$name</button>\n"
done < "$buttons_file"

# Заменяем содержимое <div class="menu">...</div>
awk -v buttons="$buttons" '
  /<div class="menu">/ {
    print
    in_menu = 1
    next
  }

  in_menu && /<\/div>/ {
    printf("%s", buttons)
    print
    in_menu = 0
    next
  }

  !in_menu
' "$input_file" > "$output_file"
