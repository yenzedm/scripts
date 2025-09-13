def calculate_savings(monthly_deposit, annual_rate, months):
    """
    Calculates future value of investments with monthly contributions and compound interest.
    """
    monthly_rate = annual_rate / 100 / 12
    balance = 0
    
    for month in range(1, months + 1):
        balance += monthly_deposit
        balance *= (1 + monthly_rate)
    
    return {
        'total_deposits': monthly_deposit * months,
        'total_interest': balance - monthly_deposit * months,
        'final_amount': balance,
        'monthly_rate': monthly_rate
    }

def display_results(data, monthly_deposit, annual_rate, months):
    """Displays calculation results in user-friendly format"""
    years = months / 12
    
    print("\nSavings Calculation Results")
    print("=" * 50)
    print(f"Monthly contribution: {monthly_deposit:,.2f}")
    print(f"Annual interest rate: {annual_rate:.2f}%")
    print(f"Investment period: {months} months ({years:.1f} years)")
    print("-" * 50)
    print(f"Total contributions: {data['total_deposits']:,.2f}")
    print(f"Interest earned: {data['total_interest']:,.2f}")
    print(f"Final balance: {data['final_amount']:,.2f}")
    print("=" * 50)

    actual_annual_return = (data['final_amount'] / data['total_deposits'] - 1) * 12/months
    print(f"Actual annualized return on contributions: {actual_annual_return * 100:.2f}%")

def main():
    print("Compound Interest Savings Calculator")
    print("-----------------------------------")
    
    try:
        monthly = float(input("Enter monthly contribution amount: "))
        rate = float(input("Enter annual interest rate (%): "))
        period = int(input("Enter investment period (months): "))
        
        if monthly <= 0 or rate < 0 or period <= 0:
            raise ValueError("All values must be positive")
        
        results = calculate_savings(monthly, rate, period)
        display_results(results, monthly, rate, period)
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
