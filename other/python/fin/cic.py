def calculate_compound_interest(principal, rate, years, compounding_freq=1):
    """
    Calculate future value with compound interest
    Formula: A = P * (1 + r/n)^(n*t)
    """
    rate_decimal = rate / 100
    return principal * (1 + rate_decimal/compounding_freq) ** (compounding_freq * years)

def display_results(principal, rate, years, freq, future_value):
    """Display formatted results with currency conversion"""
    interest = future_value - principal
    
    print("\n" + "="*40)
    print(f"{'Compound Interest Results':^40}")
    print("="*40)
    print(f"{'Initial amount:':<20} {principal:,.2f}")
    print(f"{'Annual rate:':<20} {rate}%")
    print(f"{'Years invested:':<20} {years}")
    print(f"{'Compounding freq:':<20} {freq}/year")
    print("-"*40)
    print(f"{'Future value:':<20} {future_value:,.2f}")
    print(f"{'Interest earned:':<20} {interest:,.2f}")
    print("="*40)

def main():
    try:     
        # Get inputs
        principal = float(input(f"Enter initial amount: "))
        rate = float(input("Enter annual interest rate (%): "))
        years = int(input("Enter number of years: "))
        freq = int(input("Compounding frequency per year (1=annually, 12=monthly): "))
        
        # Calculate
        future_value = calculate_compound_interest(principal, rate, years, freq)   
        
        # Display results
        display_results(principal, rate, years, freq, future_value)
        
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
