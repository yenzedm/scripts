import os
import sys


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


def read_from_file(filename):
    """
    Читает данные из файла
    Формат файла: каждая строка содержит 'цена количество'
    """
    data = []
    errors = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        print(f"Чтение файла: {filename}")
        print(f"Найдено строк: {len(lines)}")
        print("-" * 50)

        for i, line in enumerate(lines, 1):
            line = line.strip()

            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue

            parts = line.split()

            if len(parts) != 2:
                errors.append(f"Строка {i}: неверный формат - '{line}'")
                continue

            try:
                price = parse_number(parts[0])
                quantity = parse_number(parts[1])

                if price < 0 or quantity < 0:
                    errors.append(f"Строка {i}: отрицательные значения - '{line}'")
                    continue

                if quantity == 0:
                    errors.append(f"Строка {i}: количество равно 0 - '{line}'")
                    continue

                data.append((price, quantity))
                print(f"✓ Строка {i}: цена={price}, количество={quantity}")

            except ValueError:
                errors.append(f"Строка {i}: ошибка преобразования чисел - '{line}'")
            except Exception as e:
                errors.append(f"Строка {i}: ошибка - {e}")

    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден!")
        return None, None
    except PermissionError:
        print(f"Ошибка: нет доступа к файлу '{filename}'!")
        return None, None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None, None

    return data, errors


def calculate_average():
    """
    Функция для ввода цен и количеств до ввода 'stop',
    с последующим расчетом среднего значения.
    """
    total_sum = 0
    total_quantity = 0
    count = 0

    print("\nРЕЖИМ РУЧНОГО ВВОДА")
    print("=" * 50)
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

            if quantity == 0:
                print("Внимание: количество равно 0 - запись пропущена")
                continue

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

    # Вывод результатов
    print_results(count, total_sum, total_quantity, "ручного ввода")


def calculate_from_file():
    """
    Режим чтения данных из файла
    """
    print("\nРЕЖИМ ЧТЕНИЯ ИЗ ФАЙЛА")
    print("=" * 50)
    print("Формат файла: каждая строка содержит 'цена количество'")
    print("Пример содержимого файла:")
    print("  100.5 10")
    print("  200,25 5")
    print("  150 3")
    print("  # Это комментарий")
    print("-" * 50)

    # Запрос имени файла
    filename = input("Введите имя файла (или полный путь к файлу): ").strip()

    if not filename:
        print("Имя файла не может быть пустым!")
        return

    # Проверка существования файла
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не найден!")
        print("Проверьте:")
        print("1. Правильность имени файла")
        print("2. Полный путь к файлу (например: C:\\data\\prices.txt или /home/user/data.txt)")
        print("3. Что файл существует в текущей директории")

        # Показать текущую директорию
        current_dir = os.getcwd()
        print(f"\nТекущая директория: {current_dir}")

        # Показать файлы в текущей директории
        try:
            files = [f for f in os.listdir(current_dir) if os.path.isfile(f)]
            if files:
                print("\nДоступные файлы в текущей директории:")
                for file in sorted(files)[:20]:  # Показываем первые 20 файлов
                    print(f"  - {file}")
                if len(files) > 20:
                    print(f"  ... и ещё {len(files) - 20} файлов")
        except:
            pass

        return

    # Чтение данных из файла
    data, errors = read_from_file(filename)

    if data is None:
        return

    if not data:
        print("\nВ файле не найдено корректных данных!")
        return

    # Расчет результатов
    total_sum = sum(price * quantity for price, quantity in data)
    total_quantity = sum(quantity for _, quantity in data)
    count = len(data)

    # Вывод ошибок, если они есть
    if errors:
        print("\n" + "!" * 50)
        print("ОБНАРУЖЕНЫ ОШИБКИ В ФАЙЛЕ:")
        for error in errors:
            print(f"  {error}")
        print(f"Всего ошибок: {len(errors)}")
        print("!" * 50)

    # Вывод результатов
    print_results(count, total_sum, total_quantity, f"файла '{filename}'")

    # Сохранение результатов в файл (опционально)
    save_results = input("\nСохранить результаты в файл? (да/нет): ").strip().lower()
    if save_results in ['да', 'д', 'yes', 'y']:
        save_to_file(filename, count, total_sum, total_quantity)


def save_to_file(original_filename, count, total_sum, total_quantity):
    """
    Сохраняет результаты расчета в файл
    """
    if total_quantity > 0:
        average = total_sum / total_quantity

    # Создаем имя для файла результатов
    base_name = os.path.splitext(original_filename)[0]
    result_filename = f"{base_name}_results.txt"

    try:
        with open(result_filename, 'w', encoding='utf-8') as file:
            file.write("РЕЗУЛЬТАТЫ РАСЧЕТА СРЕДНЕЙ ЦЕНЫ\n")
            file.write("=" * 50 + "\n")
            file.write(f"Исходный файл: {original_filename}\n")
            file.write(f"Дата расчета: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("-" * 50 + "\n")
            file.write(f"Всего записей: {count}\n")
            file.write(f"Общая сумма: {total_sum:,.2f}\n")
            file.write(f"Общее количество: {total_quantity:,.2f}\n")
            if total_quantity > 0:
                file.write(f"Средняя цена за единицу: {average:,.4f}\n")
            file.write("=" * 50 + "\n")

        print(f"Результаты сохранены в файл: {result_filename}")
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")


def print_results(count, total_sum, total_quantity, source_name):
    """
    Выводит результаты расчета
    """
    if count == 0:
        print(f"\nНе было введено ни одной записи из {source_name}.")
        return

    if total_quantity > 0:
        average = total_sum / total_quantity

        print("\n" + "=" * 60)
        print(f"РЕЗУЛЬТАТЫ РАСЧЕТА (из {source_name})")
        print("=" * 60)
        print(f"{'Всего записей:':<25} {count:>15}")
        print(f"{'Общая сумма:':<25} {total_sum:>15,.2f}")
        print(f"{'Общее количество:':<25} {total_quantity:>15,.2f}")
        print(f"{'Средняя цена за единицу:':<25} {average:>15,.6f}")
        print("=" * 60)

        # Дополнительная информация
        print("\nДополнительная информация:")
        print(f"• Средневзвешенная цена: {average:.8f}")
        print(f"• Итоговая стоимость: {total_sum:,.2f}")

        if count > 1:
            print(f"• Минимальная цена для достижения суммы: {total_sum/total_quantity:.6f}")
    else:
        print(f"\nОшибка: общее количество равно нулю в данных из {source_name}!")


def create_example_file():
    """
    Создает пример файла с данными
    """
    example_content = """# Пример файла данных для расчета средней цены
# Формат: цена количество
# Разделитель - пробел
# Поддерживаются оба формата чисел: с точкой и с запятой

100.50 10
200,25 5
150 3
75.5 20
300 2
0,111 41036
99.99 15

# Комментарии игнорируются
# Пустые строки также игнорируются"""

    filename = "example_data.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(example_content)

        print(f"Создан пример файла: {filename}")
        print(f"Файл создан в директории: {os.getcwd()}")
        print("\nСодержимое файла:")
        print("-" * 40)
        print(example_content)
        print("-" * 40)
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")


def show_help():
    """
    Показывает справку по использованию скрипта
    """
    print("\nСПРАВКА ПО ИСПОЛЬЗОВАНИЮ СКРИПТА")
    print("=" * 60)
    print("\n1. РЕЖИМ РУЧНОГО ВВОДА:")
    print("   - Вводите данные в формате: цена количество")
    print("   - Пример: '100.5 10' или '200,25 5'")
    print("   - Для завершения введите 'stop'")
    print("\n2. РЕЖИМ ЧТЕНИЯ ИЗ ФАЙЛА:")
    print("   - Подготовьте файл с данными")
    print("   - Каждая строка: цена пробел количество")
    print("   - Поддерживаются комментарии (строки начинающиеся с #)")
    print("   - Поддерживаются пустые строки")
    print("\n3. ФОРМАТ ЧИСЕЛ:")
    print("   - Можно использовать точку: 0.111")
    print("   - Можно использовать запятую: 0,111")
    print("   - Разделитель тысяч не поддерживается")
    print("\n4. ПРИМЕР ФАЙЛА:")
    print("   Используйте опцию '4' в меню для создания примера файла")


# Импорт для даты
from datetime import datetime

# Основная программа
if __name__ == "__main__":
    print("СКРИПТ ДЛЯ РАСЧЕТА СРЕДНЕЙ ЦЕНЫ")
    print("=" * 60)

    while True:
        # Выбор режима
        print("\nГЛАВНОЕ МЕНЮ:")
        print("1 - Ручной ввод данных")
        print("2 - Чтение данных из файла")
        print("3 - Создать пример файла")
        print("4 - Показать справку")
        print("0 - Выход")

        choice = input("\nВыберите действие (0-4): ").strip()

        if choice == '1':
            calculate_average()
        elif choice == '2':
            calculate_from_file()
        elif choice == '3':
            create_example_file()
        elif choice == '4':
            show_help()
        elif choice == '0':
            print("\nВыход из программы...")
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")

        input("\nНажмите Enter для продолжения...")


# Пример функции для пакетной обработки нескольких файлов
def batch_process_files():
    """
    Обработка нескольких файлов (дополнительная функция)
    """
    print("\nПАКЕТНАЯ ОБРАБОТКА ФАЙЛОВ")
    print("=" * 50)

    # Можно добавить логику для обработки нескольких файлов
    # Например, обработка всех .txt файлов в директории
    print("Эта функция находится в разработке...")
    print("В текущей версии используйте режим 2 для обработки одного файла")
