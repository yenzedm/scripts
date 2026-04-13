CD_MENU_LIST=(
  "/home/user|Каталог пользователя user"
  "/var/log|Системные логи"
  "/tmp|Временные файлы"
)

cdm() {
  local -a menu_items=("${CD_MENU_LIST[@]}")
  local -a paths=()
  local -a tags=()
  local sep="|"                     # разделитель пути и тега
  local item path tag

  # Разбор элементов массива на путь и тег
  for item in "${menu_items[@]}"; do
    if [[ "$item" == *"$sep"* ]]; then
      path="${item%%$sep*}"         # всё до первого разделителя
      tag="${item#*$sep}"           # всё после первого разделителя
    else
      path="$item"
      tag=""
    fi
    paths+=("$path")
    tags+=("$tag")
  done

  # Вывод меню с тегами
  echo "Куда переходим?"
  for i in "${!paths[@]}"; do
    if [[ -n "${tags[i]}" ]]; then
      printf "%2d) %s (%s)\n" $((i+1)) "${paths[i]}" "${tags[i]}"
    else
      printf "%2d) %s\n" $((i+1)) "${paths[i]}"
    fi
  done

  # Ввод и проверка номера
  read -p "Введите номер: " choice
  if [[ ! "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt "${#paths[@]}" ]; then
    echo "Ошибка: неверный номер." >&2
    return 1
  fi

  # Переход в выбранный путь
  local target="${paths[$((choice-1))]}"
  cd "$target"
  echo "Перешёл в: $target"
}
