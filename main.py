import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from migration import MigrationAnalyzer
from population import PopulationAnalyzer

class DemographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Демографический анализ России")
        self.root.geometry("650x600")
        self.root.resizable(False, False)
        
        # Цвета
        BG_COLOR = "#f0f0f0"
        BTN_MIGRATION = "#87CEEB"  
        BTN_POPULATION = "#90EE90" 
        BTN_EXIT = "#F08080"  
        
        self.root.configure(bg=BG_COLOR)
        
        # Заголовок
        title = tk.Label(root, text="ДЕМОГРАФИЧЕСКИЙ АНАЛИЗ РОССИИ", 
                         font=("Arial", 18, "bold"), fg="#2c3e50", bg=BG_COLOR)
        title.pack(pady=20)
        
        # Рамка для кнопок
        frame_buttons = tk.Frame(root, bg=BG_COLOR)
        frame_buttons.pack(pady=10)
        
        # Кнопка для анализа миграции
        btn_migration = tk.Button(frame_buttons, text=" Анализ миграции населения\n(Вика)", 
                                  font=("Arial", 12, "bold"), bg=BTN_MIGRATION, 
                                  width=25, height=2, relief=tk.RAISED, bd=3,
                                  command=self.run_migration)
        btn_migration.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Кнопка для анализа населения
        btn_population = tk.Button(frame_buttons, text=" Анализ численности населения\n(Ульяна)", 
                                   font=("Arial", 12, "bold"), bg=BTN_POPULATION, 
                                   width=25, height=2, relief=tk.RAISED, bd=3,
                                   command=self.run_population)
        btn_population.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Кнопка выхода
        btn_exit = tk.Button(root, text=" Выход", font=("Arial", 11, "bold"), 
                             bg=BTN_EXIT, width=20, height=1, relief=tk.RAISED, bd=2,
                             command=root.quit)
        btn_exit.pack(pady=20)
        
        # Текстовое поле для вывода информации
        self.text_output = scrolledtext.ScrolledText(root, height=15, width=75, 
                                                      font=("Courier", 10), 
                                                      wrap=tk.WORD, bg="white", fg="black")
        self.text_output.pack(pady=10, padx=20)
        
        # Начальное сообщение
        self.log("ДОБРО ПОЖАЛОВАТЬ В ПРОГРАММУ ДЕМОГРАФИЧЕСКОГО АНАЛИЗА")
        self.log("\nВыберите нужный анализ, нажав на соответствующую кнопку.")
        self.log("После выбора файла с данными программа выполнит:\n")
        self.log("  1. Вывод таблицы данных")
        self.log("  2. Расчет максимального процента изменения")
        self.log("  3. Построение графиков")
        self.log("  4. Прогнозирование на N лет методом скользящей средней")
        self.log("\n")
    
    def log(self, message):
        """Вывод сообщения в текстовое поле"""
        self.text_output.insert(tk.END, message + "\n")
        self.text_output.see(tk.END)
        self.root.update()
    
    def clear_output(self):
        """Очистка текстового поля"""
        self.text_output.delete(1.0, tk.END)
    
    def run_migration(self):
        """Запуск анализа миграции"""
        self.clear_output()
        self.log(" Запуск анализа миграции населения...")
        
        filepath = filedialog.askopenfilename(
            title="Выберите CSV файл с данными о миграции",
            filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")]
        )
        
        if not filepath:
            self.log(" Файл не выбран. Анализ отменен.")
            return
        
        self.log(f" Выбран файл: {filepath}")
        
        try:
            analyzer = MigrationAnalyzer(filepath)
            
            # Перенаправляем вывод в GUI
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            analyzer.run()
            
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            self.log("\n")
            self.log(" РЕЗУЛЬТАТЫ АНАЛИЗА МИГРАЦИИ:")
            self.log("\n")
            self.log(output)
            
            self.log("\nАнализ миграции завершен успешно!")
            
        except Exception as e:
            self.log(f"\n ОШИБКА: {e}")
            messagebox.showerror("Ошибка", f"Не удалось выполнить анализ миграции:\n{e}")
    
    def run_population(self):
        """Запуск анализа населения"""
        self.clear_output()
        self.log(" Запуск анализа численности населения...")
        
        filepath = filedialog.askopenfilename(
            title="Выберите CSV файл с данными о численности населения",
            filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")]
        )
        
        if not filepath:
            self.log(" Файл не выбран. Анализ отменен.")
            return
        
        self.log(f" Выбран файл: {filepath}")
        
        try:
            analyzer = PopulationAnalyzer(filepath)
            
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            analyzer.run()
            
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            self.log("\n")
            self.log(" РЕЗУЛЬТАТЫ АНАЛИЗА ЧИСЛЕННОСТИ НАСЕЛЕНИЯ:")
            self.log("\n")
            self.log(output)
            
            self.log("\nАнализ численности населения завершен успешно!")
            
        except Exception as e:
            self.log(f"\n ОШИБКА: {e}")
            messagebox.showerror("Ошибка", f"Не удалось выполнить анализ населения:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DemographyApp(root)
    root.mainloop()
