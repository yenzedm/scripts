def calculate_final_amount():
    """Рассчитывает итоговую сумму на вкладе с ежемесячным пополнением."""
    
    print("=" * 50)
    print("КАЛЬКУЛЯТОР ВКЛАДА С ЕЖЕМЕСЯЧНЫМ ПОПОЛНЕНИЕМ")
    print("=" * 50)
    
    try:
        # Ввод исходных данных
        current_amount = float(input("Сколько денег у вас сейчас на вкладе? (руб.): "))
        current_rate = float(input("Под какой процент сейчас лежат деньги? (% годовых): "))
        monthly_payment = float(input("Какую сумму можете откладывать ежемесячно? (руб.): "))
        new_rate = float(input("Какой будет процент по новому вкладу? (% годовых): "))
        
        # Выбор частоты начисления процентов
        print("\nКак начисляются проценты?")
        print("1 - Ежемесячно")
        print("2 - Ежегодно")
        interest_type = int(input("Выберите вариант (1 или 2): "))
        
        months = int(input("На какой срок готовы пополнять вклад? (месяцев): "))
        
        # Проверка ввода
        if months <= 0:
            print("Срок должен быть положительным числом!")
            return
        
        if interest_type not in [1, 2]:
            print("Некорректный выбор типа начисления процентов!")
            return
        
        # Инициализация переменных
        total_amount = current_amount
        monthly_rate = new_rate / 100 / 12  # Месячная процентная ставка
        annual_rate = new_rate / 100  # Годовая процентная ставка
        
        print("\n" + "=" * 50)
        print("РАСЧЕТ НАКОПЛЕНИЙ")
        print("=" * 50)
        
        # Расчет в зависимости от типа начисления процентов
        if interest_type == 1:  # Ежемесячное начисление
            print(f"\nМесяц | Сумма на начало | Начислено % | Пополнение | Итоговая сумма")
            print("-" * 65)
            
            for month in range(1, months + 1):
                # Начисление процентов на текущую сумму
                interest_earned = total_amount * monthly_rate
                
                # Пополнение вклада
                total_amount += interest_earned + monthly_payment
                
                # Вывод информации за месяц
                print(f"{month:5d} | {total_amount - monthly_payment - interest_earned:14.2f} | "
                      f"{interest_earned:11.2f} | {monthly_payment:10.2f} | {total_amount:14.2f}")
        
        else:  # Ежегодное начисление
            print(f"\nМесяц | Сумма на начало | Пополнение | Итоговая сумма")
            print("-" * 55)
            
            for month in range(1, months + 1):
                # Пополнение вклада
                total_amount += monthly_payment
                
                # Начисление процентов в конце года
                if month % 12 == 0:
                    interest_earned = total_amount * annual_rate
                    total_amount += interest_earned
                    print(f"Годовое начисление процентов: +{interest_earned:.2f} руб.")
                
                # Вывод информации за месяц
                print(f"{month:5d} | {total_amount - monthly_payment:14.2f} | "
                      f"{monthly_payment:10.2f} | {total_amount:14.2f}")
        
        # Расчет итогов
        total_invested = current_amount + (monthly_payment * months)
        total_interest = total_amount - total_invested
        
        print("\n" + "=" * 50)
        print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
        print("=" * 50)
        print(f"Начальная сумма: {current_amount:,.2f} руб.")
        print(f"Ежемесячное пополнение: {monthly_payment:,.2f} руб.")
        print(f"Срок пополнения: {months} месяцев ({months/12:.1f} лет)")
        print(f"Процентная ставка: {new_rate}% годовых")
        print(f"Способ начисления: {'ежемесячно' if interest_type == 1 else 'ежегодно'}")
        print("-" * 50)
        print(f"Всего внесено средств: {total_invested:,.2f} руб.")
        print(f"Начислено процентов: {total_interest:,.2f} руб.")
        print(f"ИТОГОВАЯ СУММА: {total_amount:,.2f} руб.")
        print("=" * 50)
        
        # Дополнительная информация
        print(f"\nДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:")
        print(f"Доходность: {(total_interest/total_invested*100):.1f}% от внесенных средств")
        print(f"Среднемесячный доход: {(total_interest/months):.2f} руб.")
        
    except ValueError:
        print("Ошибка! Пожалуйста, вводите только числа.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def main():
    """Основная функция программы."""
    while True:
        calculate_final_amount()
        
        # Запрос на продолжение
        print("\n" + "=" * 50)
        choice = input("Хотите сделать еще один расчет? (да/нет): ").lower()
        
        if choice not in ['да', 'д', 'yes', 'y']:
            print("Спасибо за использование калькулятора! До свидания!")
            break
        print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
