import sys
from migration import MigrationAnalyzer

def print_menu():
    print("\n" + "="*50)
    print("ДЕМОГРАФИЧЕСКИЙ АНАЛИЗ РОССИИ")
    print("="*50)
    print("1. Анализ миграции населения (Вика)")
    print("0. Выход")

def main():
    while True:
        print_menu()
        choice = input("\nВыберите задание: ")
        if choice == "1":
            filepath = input("Введите путь к CSV файлу: ")
            try:
                analyzer = MigrationAnalyzer(filepath)
                analyzer.run()
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            print("До свидания!")
            sys.exit(0)

if __name__ == "__main__":
    main()