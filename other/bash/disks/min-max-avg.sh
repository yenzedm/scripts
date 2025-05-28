#!/bin/bash

if [[ "$#" -eq 0 ]]; then
    echo "use $0 -m iostat|vmstat -f path/to/file"
    exit 0
fi

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -m|--mode)
            if [[ -z "$2" ]]; then
                echo "Ошибка: опция -m|--mode требует значение"
                exit 1
            fi
            mode="$2"
            if [[ "$mode" != "iostat" && "$mode" != "vmstat" ]]; then
                echo "Ошибка: значение для -m|--mode должно быть 'iostat' или 'vmstat'"
                exit 1
            fi
            shift 2
            ;;
        -f|--file)
            if [[ -z "$2" ]]; then
                echo "Ошибка: опция -f|--file требует значение"
                exit 1
            fi
            file="$2"
            if [[ ! -f "$file" ]]; then
                echo "Ошибка: файл '$file' не существует или не является файлом"
                exit 1
            fi
            shift 2
            ;;
        -h|--help)
            echo "use $0 -m iostat|vmstat -f path/to/file"
            exit 0
            ;;
        *)
            echo "Неизвестный параметр: $1"
            exit 1
            ;;
    esac
done

# Проверяем параметры
if [ "$mode" == "iostat" ]; then
    echo "iostat info"
    echo 'r_await'
    avg=$(cat $file | awk '{print $6}' | xargs -n 4 | awk '{print $1, $3 "\n" $2, $4}' | awk '{print $2}' | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | awk '{sum += $1; count++} END {printf "%.2f\n", sum/count}')
    min=$(cat $file | awk '{print $6}' | xargs -n 4 | awk '{print $1, $3 "\n" $2, $4}' | awk '{print $2}' | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | head -n 1)
    max=$(cat $file | awk '{print $6}' | xargs -n 4 | awk '{print $1, $3 "\n" $2, $4}' | awk '{print $2}' | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | tail -n 1)
    echo "min = $min"
    echo "max = $max"
    echo "avg = $avg"
    echo 'w_await'
    avg=$(cat tmp.txt | awk '{print $12}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | awk '{sum += $1; count++} END {printf "%.2f\n", sum/count}')
    min=$(cat tmp.txt | awk '{print $12}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | head -n 1)
    max=$(cat tmp.txt | awk '{print $12}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | tail -n 1)
    echo "min = $min"
    echo "max = $max"
    echo "avg = $avg"
elif [ "$mode" == "vmstat" ]; then
    echo "vmstat info"
fi

