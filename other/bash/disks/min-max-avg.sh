#!/bin/bash

if [[ "$#" -eq 0 ]]; then
    echo "use $0 -m iostat|vmstat -f path/to/file"
    exit 0
fi

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -m|--mode)
            if [[ -z "$2" ]]; then
                echo "Error: the -m|--mode option requires a value"
                exit 1
            fi
            mode="$2"
            if [[ "$mode" != "iostat" && "$mode" != "vmstat" ]]; then
                echo "Error: value for -m|--mode must be 'iostat' or 'vmstat'"
                exit 1
            fi
            shift 2
            ;;
        -f|--file)
            if [[ -z "$2" ]]; then
                echo "Error: option -f|--file requires a value"
                exit 1
            fi
            file="$2"
            if [[ ! -f "$file" ]]; then
                echo "Error: file '$file' does not exist or is not a file"
                exit 1
            fi
            shift 2
            ;;
        -h|--help)
            echo "use $0 -m iostat|vmstat -f path/to/file"
            exit 0
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

if [ "$mode" == "iostat" ]; then
    echo "iostat info"
    echo 'r_await'
    avg=$(cat $file | tail -n +3 | awk '{print $6}' | xargs -n 4 | awk '{print $1, $3 "\n" $2, $4}' | awk '{print $2}' | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | awk '{sum += $1; count++} END {printf "%.2f\n", sum/count}')
    min=$(cat $file | tail -n +3 | awk '{print $6}' | xargs -n 4 | awk '{print $1, $3 "\n" $2, $4}' | awk '{print $2}' | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | head -n 1)
    max=$(cat $file | tail -n +3 | awk '{print $6}' | xargs -n 4 | awk '{print $1, $3 "\n" $2, $4}' | awk '{print $2}' | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | tail -n 1)
    echo "min = $min"
    echo "max = $max"
    echo "avg = $avg"
    echo 'w_await'
    avg=$(cat $file  | tail -n +3 | awk '{print $12}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | awk '{sum += $1; count++} END {printf "%.2f\n", sum/count}')
    min=$(cat $file  | tail -n +3 | awk '{print $12}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | head -n 1)
    max=$(cat $file  | tail -n +3 | awk '{print $12}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | tail -n 1)
    echo "min = $min"
    echo "max = $max"
    echo "avg = $avg"
    echo 'aqu-sz'
    avg=$(cat $file  | tail -n +3 | awk '{print $22}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | awk '{sum += $1; count++} END {printf "%.2f\n", sum/count}')
    min=$(cat $file  | tail -n +3 | awk '{print $22}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | head -n 1)
    max=$(cat $file  | tail -n +3 | awk '{print $22}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | tail -n 1)
    echo "min = $min"
    echo "max = $max"
    echo "avg = $avg"
    echo 'util'
    avg=$(cat $file  | tail -n +3 | awk '{print $23}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | awk '{sum += $1; count++} END {printf "%.2f\n", sum/count}')
    min=$(cat $file  | tail -n +3 | awk '{print $23}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | head -n 1)
    max=$(cat $file  | tail -n +3 | awk '{print $23}' | tail -n +4 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | tail -n 1)
    echo "min = $min"
    echo "max = $max"
    echo "avg = $avg"
    echo 'iowait'
    avg=$(cat $file  | tail -n +3 | awk '{print $4}' | xargs -n 4 | awk '{print $1, $3 "\n" $2, $4}' | awk '{print $1}' | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | awk '{sum += $1; count++} END {printf "%.2f\n", sum/count}')
    min=$(cat $file  | tail -n +3 | awk '{print $4}' | xargs -n 4 | awk '{print $1, $3 "\n" $2, $4}' | awk '{print $1}' | grep -oE '[0-9]+([,.][0-9]+)?' | sort -n | head -n 1)
    max=$(cat $file  | tail -n +3 | awk '{print $4}' | xargs -n 4 | awk '{print $1, $3 "\n" $2, $4}' | awk '{print $1}' | grep -oE '[0-9]+([,.][0-9]+)?' | sort -n | tail -n 1)
    echo "min = $min"
    echo "max = $max"
    echo "avg = $avg"
elif [ "$mode" == "vmstat" ]; then
    echo 'vmstat info'
    echo 'b'
    avg=$(cat $file | awk '{print $2}' | tail -n +3 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | awk '{sum += $1; count++} END {printf "%.2f\n", sum/count}')
    min=$(cat $file | awk '{print $2}' | tail -n +3 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | head -n 1)
    max=$(cat $file | awk '{print $2}' | tail -n +3 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | tail -n 1)
    echo "min = $min"
    echo "max = $max"
    echo "avg = $avg"
    echo 'bi'
    avg=$(cat $file | awk '{print $9}' | tail -n +3 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | awk '{sum += $1; count++} END {printf "%.2f\n", sum/count}')
    min=$(cat $file | awk '{print $9}' | tail -n +3 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | head -n 1)
    max=$(cat $file | awk '{print $9}' | tail -n +3 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | tail -n 1)
    echo "min = $min"
    echo "max = $max"
    echo "avg = $avg"
    echo 'bo'
    avg=$(cat $file | awk '{print $10}' | tail -n +3 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | awk '{sum += $1; count++} END {printf "%.2f\n", sum/count}')
    min=$(cat $file | awk '{print $10}' | tail -n +3 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | head -n 1)
    max=$(cat $file | awk '{print $10}' | tail -n +3 | grep -oE '[0-9]+([,.][0-9]+)?' | sed 's/,/./g' | sort -n | tail -n 1)
    echo "min = $min"
    echo "max = $max"
    echo "avg = $avg"
fi


# iostat -x sda 3 > out_iostat.txt
# vmstat 3 > out_vmstat.txt
