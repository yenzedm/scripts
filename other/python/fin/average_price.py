import os
import sys
from datetime import datetime


def parse_number(num_str):
    """
    Converts a string to a number, supporting both decimal separators: dot and comma
    """
    # Replace comma with dot for correct conversion
    num_str = num_str.replace(',', '.')
    
    # Remove possible spaces
    num_str = num_str.strip()
    
    # Convert to float
    return float(num_str)


def read_from_file(filename):
    """
    Reads data from a file
    File format: each line contains 'price quantity'
    """
    data = []
    errors = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        print(f"Reading file: {filename}")
        print(f"Lines found: {len(lines)}")
        print("-" * 50)
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            
            if len(parts) != 2:
                errors.append(f"Line {i}: invalid format - '{line}'")
                continue
            
            try:
                price = parse_number(parts[0])
                quantity = parse_number(parts[1])
                
                if price < 0 or quantity < 0:
                    errors.append(f"Line {i}: negative values - '{line}'")
                    continue
                
                if quantity == 0:
                    errors.append(f"Line {i}: quantity is 0 - '{line}'")
                    continue
                
                data.append((price, quantity))
                print(f"✓ Line {i}: price={price}, quantity={quantity}")
                
            except ValueError:
                errors.append(f"Line {i}: number conversion error - '{line}'")
            except Exception as e:
                errors.append(f"Line {i}: error - {e}")
    
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found!")
        return None, None
    except PermissionError:
        print(f"Error: no access to file '{filename}'!")
        return None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None
    
    return data, errors


def calculate_average():
    """
    Function for entering prices and quantities until 'stop' is entered,
    then calculates the average value.
    """
    total_sum = 0
    total_quantity = 0
    count = 0
    
    print("\nMANUAL INPUT MODE")
    print("=" * 50)
    print("Enter data in format 'price quantity' (e.g., '100 5' or '0,111 41036')")
    print("Both separators supported: dot (0.111) and comma (0,111)")
    print("Enter 'stop' to finish")
    print("-" * 50)
    
    while True:
        user_input = input(f"Entry {count + 1}: ").strip().lower()
        
        # Check if user wants to stop
        if user_input == 'stop':
            break
        
        # Skip empty strings
        if not user_input:
            print("Error: input cannot be empty!")
            continue
        
        try:
            # Split input into parts
            parts = user_input.split()
            
            if len(parts) != 2:
                print("Error: enter exactly 2 values (price and quantity) separated by space!")
                continue
            
            # Convert to numbers with support for different formats
            price = parse_number(parts[0])
            quantity = parse_number(parts[1])
            
            # Check that numbers are positive
            if price < 0 or quantity < 0:
                print("Error: price and quantity must be positive!")
                continue
            
            if quantity == 0:
                print("Warning: quantity is 0 - entry skipped")
                continue
            
            # Add to total sum and quantity
            total_sum += price * quantity
            total_quantity += quantity
            count += 1
            
            print(f"✓ Added: price={price}, quantity={quantity}, amount={price * quantity:.2f}")
            
        except ValueError as e:
            print(f"Number conversion error: {e}")
            print(f"Entered: '{user_input}'")
            print("Example of correct input: '0.111 41036' or '0,111 41036'")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
    
    # Display results
    print_results(count, total_sum, total_quantity, "manual input")


def calculate_from_file():
    """
    Mode for reading data from a file
    """
    print("\nFILE READING MODE")
    print("=" * 50)
    print("File format: each line contains 'price quantity'")
    print("Example file content:")
    print("  100.5 10")
    print("  200,25 5")
    print("  150 3")
    print("  # This is a comment")
    print("-" * 50)
    
    # Ask for filename
    filename = input("Enter filename (or full file path): ").strip()
    
    if not filename:
        print("Filename cannot be empty!")
        return
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"File '{filename}' not found!")
        print("Please check:")
        print("1. Correctness of filename")
        print("2. Full file path (e.g., C:\\data\\prices.txt or /home/user/data.txt)")
        print("3. That the file exists in current directory")
        
        # Show current directory
        current_dir = os.getcwd()
        print(f"\nCurrent directory: {current_dir}")
        
        # Show files in current directory
        try:
            files = [f for f in os.listdir(current_dir) if os.path.isfile(f)]
            if files:
                print("\nAvailable files in current directory:")
                for file in sorted(files)[:20]:  # Show first 20 files
                    print(f"  - {file}")
                if len(files) > 20:
                    print(f"  ... and {len(files) - 20} more files")
        except:
            pass
        
        return
    
    # Read data from file
    data, errors = read_from_file(filename)
    
    if data is None:
        return
    
    if not data:
        print("\nNo valid data found in file!")
        return
    
    # Calculate results
    total_sum = sum(price * quantity for price, quantity in data)
    total_quantity = sum(quantity for _, quantity in data)
    count = len(data)
    
    # Display errors if any
    if errors:
        print("\n" + "!" * 50)
        print("ERRORS DETECTED IN FILE:")
        for error in errors:
            print(f"  {error}")
        print(f"Total errors: {len(errors)}")
        print("!" * 50)
    
    # Display results
    print_results(count, total_sum, total_quantity, f"file '{filename}'")
    
    # Option to save results to file
    save_results = input("\nSave results to file? (yes/no): ").strip().lower()
    if save_results in ['yes', 'y', 'да', 'д']:  # Keeping Russian options for compatibility
        save_to_file(filename, count, total_sum, total_quantity)


def save_to_file(original_filename, count, total_sum, total_quantity):
    """
    Saves calculation results to a file
    """
    if total_quantity > 0:
        average = total_sum / total_quantity
    
    # Create name for results file
    base_name = os.path.splitext(original_filename)[0]
    result_filename = f"{base_name}_results.txt"
    
    try:
        with open(result_filename, 'w', encoding='utf-8') as file:
            file.write("AVERAGE PRICE CALCULATION RESULTS\n")
            file.write("=" * 50 + "\n")
            file.write(f"Source file: {original_filename}\n")
            file.write(f"Calculation date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("-" * 50 + "\n")
            file.write(f"Total entries: {count}\n")
            file.write(f"Total sum: {total_sum:,.2f}\n")
            file.write(f"Total quantity: {total_quantity:,.2f}\n")
            if total_quantity > 0:
                file.write(f"Average price per unit: {average:,.4f}\n")
            file.write("=" * 50 + "\n")
        
        print(f"Results saved to file: {result_filename}")
    except Exception as e:
        print(f"Error saving results: {e}")


def print_results(count, total_sum, total_quantity, source_name):
    """
    Displays calculation results
    """
    if count == 0:
        print(f"\nNo entries entered from {source_name}.")
        return
    
    if total_quantity > 0:
        average = total_sum / total_quantity
        
        print("\n" + "=" * 60)
        print(f"CALCULATION RESULTS (from {source_name})")
        print("=" * 60)
        print(f"{'Total entries:':<25} {count:>15}")
        print(f"{'Total sum:':<25} {total_sum:>15,.2f}")
        print(f"{'Total quantity:':<25} {total_quantity:>15,.2f}")
        print(f"{'Average price per unit:':<25} {average:>15,.6f}")
        print("=" * 60)
        
        # Additional information
        print("\nAdditional information:")
        print(f"• Weighted average price: {average:.8f}")
        print(f"• Final cost: {total_sum:,.2f}")
        
        if count > 1:
            print(f"• Minimum price to achieve sum: {total_sum/total_quantity:.6f}")
    else:
        print(f"\nError: total quantity is zero in data from {source_name}!")


def create_example_file():
    """
    Creates an example data file
    """
    example_content = """# Example data file for average price calculation
# Format: price quantity
# Separator - space
# Both number formats supported: with dot and with comma

100.50 10
200,25 5
150 3
75.5 20
300 2
0,111 41036
99.99 15

# Comments are ignored
# Empty lines are also ignored"""
    
    filename = "example_data.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(example_content)
        
        print(f"Example file created: {filename}")
        print(f"File created in directory: {os.getcwd()}")
        print("\nFile content:")
        print("-" * 40)
        print(example_content)
        print("-" * 40)
    except Exception as e:
        print(f"Error creating file: {e}")


def show_help():
    """
    Shows usage help
    """
    print("\nSCRIPT USAGE HELP")
    print("=" * 60)
    print("\n1. MANUAL INPUT MODE:")
    print("   - Enter data in format: price quantity")
    print("   - Example: '100.5 10' or '200,25 5'")
    print("   - Enter 'stop' to finish")
    print("\n2. FILE READING MODE:")
    print("   - Prepare a data file")
    print("   - Each line: price space quantity")
    print("   - Comments supported (lines starting with #)")
    print("   - Empty lines supported")
    print("\n3. NUMBER FORMATS:")
    print("   - Dot can be used: 0.111")
    print("   - Comma can be used: 0,111")
    print("   - Thousands separator not supported")
    print("\n4. EXAMPLE FILE:")
    print("   Use option '3' in menu to create an example file")


# Main program
if __name__ == "__main__":
    print("AVERAGE PRICE CALCULATION SCRIPT")
    print("=" * 60)
    
    while True:
        # Mode selection
        print("\nMAIN MENU:")
        print("1 - Manual data input")
        print("2 - Read data from file")
        print("3 - Create example file")
        print("4 - Show help")
        print("0 - Exit")
        
        choice = input("\nSelect action (0-4): ").strip()
        
        if choice == '1':
            calculate_average()
        elif choice == '2':
            calculate_from_file()
        elif choice == '3':
            create_example_file()
        elif choice == '4':
            show_help()
        elif choice == '0':
            print("\nExiting program...")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


# Example function for batch processing multiple files
def batch_process_files():
    """
    Process multiple files (additional function)
    """
    print("\nBATCH FILE PROCESSING")
    print("=" * 50)
    
    # Logic for processing multiple files can be added here
    # For example, process all .txt files in directory
    print("This feature is under development...")
    print("In current version use mode 2 for single file processing")


# Testing function for number parsing
def test_parse_number():
    """Test the parse_number function"""
    test_cases = [
        "0.111",
        "0,111",
        "123.45",
        "123,45",
        "1000",
        "1,000.50",
        "1.000,50"
    ]
    
    print("Testing number conversion:")
    for test in test_cases:
        try:
            result = parse_number(test)
            print(f"'{test}' -> {result}")
        except Exception as e:
            print(f"'{test}' -> Error: {e}")


# For quick testing, uncomment the following line:
# test_parse_number()
