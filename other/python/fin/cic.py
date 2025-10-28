def calculate_compound_interest(principal, rate, months, compounding_freq=1):
    """
    Calculate future value with compound interest
    Formula: A = P * (1 + r/n)^(n*t)
    where t is in years (months/12)
    """
    rate_decimal = rate / 100
    years = months / 12
    return principal * (1 + rate_decimal/compounding_freq) ** (compounding_freq * years)

def display_results(principal, rate, months, freq, future_value):
    """Display formatted results with currency conversion"""
    interest = future_value - principal
    years = months / 12
    
    print("\n" + "="*40)
    print(f"{'Compound Interest Results':^40}")
    print("="*40)
    print(f"{'Initial amount:':<20} {principal:,.2f}")
    print(f"{'Annual rate:':<20} {rate}%")
    print(f"{'Months invested:':<20} {months}")
    print(f"{'Years invested:':<20} {years:.2f}")
    print(f"{'Compounding freq:':<20} {freq}/year")
    print("-"*40)
    print(f"{'Future value:':<20} {future_value:,.2f}")
    print(f"{'Interest earned:':<20} {interest:,.2f}")
    print("="*40)

def main():
    try:
        # Get inputs
        principal = float(input("Enter initial amount: "))
        rate = float(input("Enter annual interest rate (%): "))
        
        # Ask user for time unit preference
        print("\nChoose time unit:")
        print("1 - Months")
        print("2 - Years")
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "1":
            months = float(input("Enter number of months: "))
        elif choice == "2":
            years = float(input("Enter number of years: "))
            months = years * 12
        else:
            print("Invalid choice. Using months by default.")
            months = float(input("Enter number of months: "))
        
        freq = int(input("Compounding frequency per year (1=annually, 12=monthly): "))

        # Calculate
        future_value = calculate_compound_interest(principal, rate, months, freq)

        # Display results
        display_results(principal, rate, months, freq, future_value)

    except ValueError as e:
        print(f"Error: Please enter valid numbers. {str(e)}")

if __name__ == "__main__":
    main()
