def calculate_cagr(start, end, years):
    return (end / start) ** (1 / years) - 1

cagr = calculate_cagr(250000, 370000, 2)
print(f"Среднегодовой доход: {cagr * 100:.2f}%")

