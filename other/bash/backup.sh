#!/bin/bash

function print_help() {
    local script_path="$1"
    echo "Usage for creating backup: ${script_path} <source directory> <backup directory>"
    echo "Usage for getting version of manager: ${script_path} -v/--version"
    echo "Usage for recover backup: ${script_path} -r/--recover <backup file name> <recover directory>"
    echo "Note: For encrypted backups, use .sec files for recovery"
}

function print_version() {
    echo "Backup manager v1.0.2"
}

function check_args() {
    if [ "$#" -lt 2 ]; then
        echo "Error: Insufficient arguments"
        echo "Use -h or --help to see how to work with script"
        exit 1
    fi
}

function get_password() {
    read -sp "Enter encryption password: " password
    echo
    echo "$password"
}

function encrypt_file() {
    local input_file="$1"
    local output_file="$2"
    local password="$3"
    
    openssl enc -aes-256-cbc -salt -in "$input_file" -out "$output_file" -pass pass:"$password" 2>/dev/null
    return $?
}

function decrypt_file() {
    local input_file="$1"
    local output_file="$2"
    local password="$3"
    
    openssl enc -aes-256-cbc -d -in "$input_file" -out "$output_file" -pass pass:"$password" 2>/dev/null
    return $?
}

function do_recover() {
    if [ "$#" -ne 3 ]; then
        echo "Error: Recovery requires exactly 2 arguments"
        print_help "$0"
        exit 1
    fi

    local backup_file="$2"
    local recover_directory="$3"

    if [ ! -f "$backup_file" ]; then
        echo "Error: Backup file '$backup_file' does not exist"
        exit 1
    fi
    
    if [ ! -d "$recover_directory" ]; then
        echo "Error: Recovery directory '$recover_directory' does not exist"
        exit 1
    fi

    local temp_file=$(mktemp)
    local password

    # Handle encrypted backups (.sec extension)
    if [[ "$backup_file" == *.sec ]]; then
        password=$(get_password)
        if ! decrypt_file "$backup_file" "$temp_file" "$password"; then
            echo "Error: Decryption failed (wrong password?)"
            rm -f "$temp_file" 2>/dev/null
            exit 1
        fi
        backup_file="$temp_file"
    else
        # For non-encrypted backups, just use the original file
        temp_file=""
    fi

    # Verify it's a valid gzip file
    if ! gzip -t "$backup_file" 2>/dev/null; then
        echo "Error: Invalid backup file (not a gzip archive)"
        [ -n "$temp_file" ] && rm -f "$temp_file"
        exit 1
    fi

    echo "Restoring backup..."
    if tar -xzf "$backup_file" -C "$recover_directory" 2>/dev/null; then
        echo "Backup was recovered successfully"
    else
        echo "Error: Failed to extract backup"
    fi

    # Cleanup
    [ -f "$temp_file" ] && rm -f "$temp_file"
}

function create_backup() {
    if [ "$#" -ne 2 ]; then
        echo "Error: Backup creation requires exactly 2 arguments"
        print_help "$0"
        exit 1
    fi

    local source_directory="$1"
    local backup_directory="$2"
    local timestamp=$(date +'%Y%m%d_%H%M%S')
    local backup_name="backup_${timestamp}"
    local temp_file="${backup_directory}/${backup_name}.tar.gz"
    local final_file

    if [ ! -d "$source_directory" ]; then
        echo "Error: Source directory '$source_directory' does not exist"
        exit 1
    fi

    mkdir -p "$backup_directory" || {
        echo "Error: Failed to create backup directory"
        exit 1
    }

    echo "Creating backup of $source_directory..."
    if ! tar -czf "$temp_file" -C "$(dirname "$source_directory")" "$(basename "$source_directory")"; then
        echo "Error: Failed to create archive"
        rm -f "$temp_file" 2>/dev/null
        exit 1
    fi

    read -p "Encrypt backup? [y/N] " encrypt_choice
    if [[ "$encrypt_choice" =~ ^[Yy] ]]; then
        password=$(get_password)
        final_file="${backup_directory}/${backup_name}.sec"
        if encrypt_file "$temp_file" "$final_file" "$password"; then
            echo "Backup encrypted successfully"
            rm -f "$temp_file"
        else
            echo "Error: Encryption failed"
            rm -f "$final_file" 2>/dev/null
            final_file="$temp_file"
        fi
    else
        final_file="$temp_file"
    fi

    # Set immutable flag if root
    if [ "$(id -u)" -eq 0 ]; then
        chattr +i "$final_file" 2>/dev/null && \
        echo "Backup file protected (immutable flag set)"
    fi

    echo "Backup created successfully: $final_file"
    echo "Size: $(du -h "$final_file" | cut -f1)"
}

function main() {
    case "$1" in
        -h|--help)
            print_help "$0"
            exit 0
            ;;
        -v|--version)
            print_version
            exit 0
            ;;
        -r|--recover)
            shift
            do_recover "$0" "$@"
            ;;
        *)
            check_args "$@"
            create_backup "$@"
            ;;
    esac
}

# Start of the script
main "$@"
