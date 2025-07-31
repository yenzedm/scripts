def calculate_cagr(start_value, end_value, years):
    """
    Calculates the Compound Annual Growth Rate (CAGR).
    
    Parameters:
        start_value (float): Initial investment value
        end_value (float): Final investment value
        years (float): Investment period in years
        
    Returns:
        float: CAGR as decimal (e.g., 0.10 for 10%)
        
    Formula:
        CAGR = (end_value / start_value)^(1/years) - 1
        
    Raises:
        ValueError: If input values are invalid
    """
    # Validate input parameters
    if start_value <= 0:
        raise ValueError("Initial value must be positive")
    if end_value < 0:
        raise ValueError("Final value cannot be negative")
    if years <= 0:
        raise ValueError("Time period must be greater than zero")
    
    # Calculate CAGR using standard formula
    return (end_value / start_value) ** (1 / years) - 1


def format_percentage(value):
    """Formats decimal value as percentage with 2 decimal places"""
    return f"{value * 100:.2f}%"


def display_results(initial, final, period, rate):
    """Displays investment growth analysis in readable format"""
    print("\nInvestment Growth Analysis")
    print("=" * 40)
    print(f"Initial amount: {initial:,.2f} ₽")
    print(f"Final amount: {final:,.2f} ₽")
    print(f"Investment period: {period} years")
    print("-" * 40)
    print(f"Compound Annual Growth Rate (CAGR): {format_percentage(rate)}")


def main():
    # Example investment scenario
    INITIAL_INVESTMENT = int(input("Starting capital: "))  # Starting capital
    FINAL_VALUE = int(input("Value after investment period: "))         # Value after investment period
    INVESTMENT_PERIOD = int(input("Years invested: "))        # Years invested
    
    try:
        # Calculate growth rate
        growth_rate = calculate_cagr(
            start_value=INITIAL_INVESTMENT,
            end_value=FINAL_VALUE,
            years=INVESTMENT_PERIOD
        )
        
        # Display formatted results
        display_results(
            initial=INITIAL_INVESTMENT,
            final=FINAL_VALUE,
            period=INVESTMENT_PERIOD,
            rate=growth_rate
        )
        
    except ValueError as e:
        print(f"Calculation error: {e}")


if __name__ == "__main__":
    main()
