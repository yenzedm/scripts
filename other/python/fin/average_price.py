def parse_number(num_str):
    """
    Преобразует строку в число, поддерживая оба разделителя: точку и запятую
    """
    # Заменяем запятую на точку для корректного преобразования
    num_str = num_str.replace(',', '.')
    
    # Удаляем возможные пробелы
    num_str = num_str.strip()
    
    # Преобразуем в float
    return float(num_str)


def calculate_average():
    """
    Функция для ввода цен и количеств до ввода 'stop',
    с последующим расчетом среднего значения.
    """
    total_sum = 0
    total_quantity = 0
    count = 0
    
    print("Введите данные в формате 'цена количество' (например: '100 5' или '0,111 41036')")
    print("Поддерживаются оба разделителя: точка (0.111) и запятая (0,111)")
    print("Для завершения ввода введите 'stop'")
    print("-" * 50)
    
    while True:
        user_input = input(f"Запись {count + 1}: ").strip().lower()
        
        # Проверяем, хочет ли пользователь остановиться
        if user_input == 'stop':
            break
        
        # Пропускаем пустые строки
        if not user_input:
            print("Ошибка: ввод не может быть пустым!")
            continue
        
        try:
            # Разделяем ввод на части
            parts = user_input.split()
            
            if len(parts) != 2:
                print("Ошибка: введите ровно 2 значения (цена и количество) разделенные пробелом!")
                continue
            
            # Преобразуем в числа с поддержкой разных форматов
            price = parse_number(parts[0])
            quantity = parse_number(parts[1])
            
            # Проверяем, что числа положительные
            if price < 0 or quantity < 0:
                print("Ошибка: цена и количество должны быть положительными!")
                continue
            
            # Проверяем на нулевые значения (если это нужно)
            if price == 0:
                print("Внимание: цена равна 0")
            
            if quantity == 0:
                print("Внимание: количество равно 0")
                continue  # Пропускаем записи с нулевым количеством
            
            # Добавляем к общей сумме и количеству
            total_sum += price * quantity
            total_quantity += quantity
            count += 1
            
            print(f"✓ Добавлено: цена={price}, количество={quantity}, сумма={price * quantity:.2f}")
            
        except ValueError as e:
            print(f"Ошибка преобразования числа: {e}")
            print(f"Введено: '{user_input}'")
            print("Пример корректного ввода: '0.111 41036' или '0,111 41036'")
        except Exception as e:
            print(f"Произошла неожиданная ошибка: {e}")
    
    # Проверяем, были ли введены данные
    if count == 0:
        print("\nНе было введено ни одной записи.")
        return
    
    # Вычисляем среднее значение
    if total_quantity > 0:
        average = total_sum / total_quantity
        
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ:")
        print(f"Всего записей: {count}")
        print(f"Общая сумма: {total_sum:,.2f}".replace(',', ' '))
        print(f"Общее количество: {total_quantity:,.2f}".replace(',', ' '))
        print(f"Средняя цена за единицу: {average:,.4f}".replace(',', ' '))
        print("=" * 50)
        
        # Дополнительная информация
        print("\nДополнительно:")
        print(f"Средневзвешенная цена: {average:.6f}")
        print(f"Итоговая стоимость: {total_sum:.2f}")
    else:
        print("\nОшибка: общее количество равно нулю!")


def calculate_average_alternative():
    """
    Альтернативная версия с раздельным вводом цены и количества
    """
    total_sum = 0
    total_quantity = 0
    count = 0
    
    print("Введите данные по товарам. Для каждого товара укажите цену и количество.")
    print("Поддерживаются оба разделителя: точка (0.111) и запятая (0,111)")
    print("Для завершения ввода введите 'stop' вместо цены")
    print("-" * 50)
    
    while True:
        try:
            # Ввод цены
            price_input = input(f"Товар {count + 1} - цена: ").strip().lower()
            
            if price_input == 'stop':
                break
            
            if not price_input:
                print("Цена не может быть пустой!")
                continue
            
            price = parse_number(price_input)
            
            if price < 0:
                print("Цена должна быть положительной!")
                continue
            
            if price == 0:
                print("Внимание: цена равна 0")
            
            # Ввод количества
            quantity_input = input(f"Товар {count + 1} - количество: ").strip().lower()
            
            if quantity_input == 'stop':
                print("Завершение ввода...")
                break
            
            if not quantity_input:
                print("Количество не может быть пустым!")
                continue
            
            quantity = parse_number(quantity_input)
            
            if quantity < 0:
                print("Количество должно быть положительным!")
                continue
            
            if quantity == 0:
                print("Количество равно 0 - запись пропущена")
                continue
            
            # Добавляем к общей сумме и количеству
            total_sum += price * quantity
            total_quantity += quantity
            count += 1
            
            print(f"✓ Добавлено: сумма={price * quantity:.2f}")
            
        except ValueError as e:
            print(f"Ошибка: некорректное число! {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
    
    # Вывод результатов
    if count > 0 and total_quantity > 0:
        average = total_sum / total_quantity
        
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ:")
        print(f"Обработано товаров: {count}")
        print(f"Общая стоимость: {total_sum:,.2f}".replace(',', ' '))
        print(f"Общее количество: {total_quantity:,.2f}".replace(',', ' '))
        print(f"Средняя цена: {average:,.4f}".replace(',', ' '))
        print("=" * 50)
    elif count == 0:
        print("\nНе было введено ни одного товара.")
    else:
        print("\nОшибка в расчетах.")


def quick_mode():
    """
    Упрощенный режим для быстрого ввода
    """
    print("БЫСТРЫЙ РЕЖИМ")
    print("Вводите 'цена количество' или 'stop' для завершения")
    print("-" * 50)
    
    data = []
    
    while True:
        user_input = input(f"Ввод {len(data) + 1}: ").strip()
        
        if user_input.lower() == 'stop':
            break
        
        parts = user_input.split()
        if len(parts) != 2:
            print("Формат: цена количество")
            continue
        
        try:
            price = parse_number(parts[0])
            quantity = parse_number(parts[1])
            
            if price >= 0 and quantity > 0:
                data.append((price, quantity))
                print(f"OK: {price} × {quantity}")
            else:
                print("Цена ≥ 0, количество > 0")
        except:
            print("Ошибка числа")
    
    if not data:
        print("Нет данных")
        return
    
    total_sum = sum(p * q for p, q in data)
    total_quantity = sum(q for _, q in data)
    average = total_sum / total_quantity
    
    print("\nРезультат:")
    print(f"Среднее: {average:.6f}")
    print(f"Сумма: {total_sum:.2f}")
    print(f"Количество: {total_quantity}")


# Основная программа
if __name__ == "__main__":
    print("СКРИПТ ДЛЯ РАСЧЕТА СРЕДНЕЙ ЦЕНЫ")
    print("=" * 60)
    
    # Выбор режима ввода
    print("Выберите режим ввода:")
    print("1 - Ввод 'цена количество' в одной строке (рекомендуется)")
    print("2 - Раздельный ввод цены и количества")
    print("3 - Быстрый режим (минимальный вывод)")
    
    choice = input("Ваш выбор (1-3): ").strip()
    
    if choice == '1':
        calculate_average()
    elif choice == '2':
        calculate_average_alternative()
    elif choice == '3':
        quick_mode()
    else:
        print("Неверный выбор. Запускаю режим по умолчанию...")
        calculate_average()
    
    input("\nНажмите Enter для выхода...")


# Дополнительная функция для тестирования
def test_parse_number():
    """Тестирование функции parse_number"""
    test_cases = [
        "0.111",
        "0,111",
        "123.45",
        "123,45",
        "1000",
        "1,000.50",
        "1.000,50"
    ]
    
    print("Тестирование преобразования чисел:")
    for test in test_cases:
        try:
            result = parse_number(test)
            print(f"'{test}' -> {result}")
        except Exception as e:
            print(f"'{test}' -> Ошибка: {e}")


# Для быстрого теста можно раскомментировать следующую строку:
# test_parse_number()
