import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class PopulationAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None
    
    def load_data(self):
        self.data = pd.read_csv(self.filepath)
        if 'год' not in self.data.columns or 'численность' not in self.data.columns:
            raise ValueError("Файл должен содержать колонки: год, численность")
        print(f"Загружено {len(self.data)} записей")
    
    def display_table(self):
        print("\n" + "="*60)
        print("ЧИСЛЕННОСТЬ НАСЕЛЕНИЯ РОССИИ")
        print("="*60)
        print(f"{'Год':<6} {'Численность (чел)':<20}")
        print("-"*60)
        for _, row in self.data.iterrows():
            print(f"{row['год']:<6} {row['численность']:<20,}")
        input("\nНажмите Enter...")
    
    def max_growth_decrease(self):
        population = self.data['численность'].values
        max_growth = 0
        max_decrease = 0
        year_growth = year_decrease = None
        for i in range(1, len(population)):
            pct = (population[i] - population[i-1]) / population[i-1] * 100
            if pct > max_growth:
                max_growth = pct
                year_growth = self.data['год'].iloc[i]
            if pct < max_decrease:
                max_decrease = pct
                year_decrease = self.data['год'].iloc[i]
        print(f"\nМакс. прирост: {max_growth:.2f}% ({year_growth} г.)")
        print(f"Макс. убыль: {max_decrease:.2f}% ({year_decrease} г.)")
        input("\nНажмите Enter...")
    
    def plot_data(self):
        plt.figure(figsize=(10,6))
        plt.plot(self.data['год'], self.data['численность'], 'go-', linewidth=2, markersize=8)
        plt.xlabel('Год')
        plt.ylabel('Численность (чел)')
        plt.title('Динамика численности населения России')
        plt.grid(True)
        plt.show()
        input("Нажмите Enter...")
    
    def moving_average_forecast(self, data, n_years, window=3):
        forecast = []
        current = list(data)
        for _ in range(n_years):
            avg = np.mean(current[-window:])
            forecast.append(avg)
            current.append(avg)
        return forecast
    
    def forecast(self):
        n = int(input("На сколько лет прогноз? "))
        window = int(input("Окно скользящей средней? "))
        years = self.data['год'].values
        last_year = years[-1]
        forecast_years = list(range(last_year+1, last_year+n+1))
        
        pop_forecast = self.moving_average_forecast(self.data['численность'].values, n, window)
        
        print("\nПРОГНОЗ ЧИСЛЕННОСТИ:")
        for i, y in enumerate(forecast_years):
            print(f"{y}: {pop_forecast[i]:.0f} чел.")
        
        plt.figure(figsize=(12,6))
        plt.plot(years, self.data['численность'], 'go-', label='Исторические данные')
        plt.plot(forecast_years, pop_forecast, 'r--o', label='Прогноз')
        plt.axvspan(forecast_years[0]-0.5, forecast_years[-1]+0.5, alpha=0.2, color='gray')
        plt.xlabel('Год')
        plt.ylabel('Численность (чел)')
        plt.title('Численность населения с прогнозом')
        plt.legend()
        plt.grid(True)
        plt.show()
        input("Нажмите Enter...")
    
    def run(self):
        self.load_data()
        self.display_table()
        self.max_growth_decrease()
        self.plot_data()
        self.forecast()