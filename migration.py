import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class MigrationAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None
    
    def load_data(self):
        self.data = pd.read_csv(self.filepath)
        if 'год' not in self.data.columns or 'иммигранты' not in self.data.columns or 'эмигранты' not in self.data.columns:
            raise ValueError("Файл должен содержать колонки: год, иммигранты, эмигранты")
        print(f"Загружено {len(self.data)} записей")
    
    def display_table(self):
        print("\n" + "="*80)
        print("МИГРАЦИЯ НАСЕЛЕНИЯ РОССИИ")
        print("="*80)
        print(f"{'Год':<6} {'Иммигранты':<12} {'Эмигранты':<12} {'Сальдо':<12}")
        print("-"*80)
        for _, row in self.data.iterrows():
            saldo = row['иммигранты'] - row['эмигранты']
            print(f"{row['год']:<6} {row['иммигранты']:<12,} {row['эмигранты']:<12,} {saldo:<12,}")
        input("\nНажмите Enter...")
    
    def max_change_percent(self):
        immigrants = self.data['иммигранты'].values
        emigrants = self.data['эмигранты'].values
        total_flow = immigrants + emigrants
        max_increase = 0
        max_decrease = 0
        year_inc = year_dec = None
        for i in range(1, len(total_flow)):
            pct = (total_flow[i] - total_flow[i-1]) / total_flow[i-1] * 100
            if pct > max_increase:
                max_increase = pct
                year_inc = self.data['год'].iloc[i]
            if pct < max_decrease:
                max_decrease = pct
                year_dec = self.data['год'].iloc[i]
        print(f"\nМакс. рост: {max_increase:.2f}% ({year_inc} г.)")
        print(f"Макс. спад: {max_decrease:.2f}% ({year_dec} г.)")
        input("\nНажмите Enter...")
    
    def plot_data(self):
        years = self.data['год']
        plt.figure(figsize=(10,6))
        plt.plot(years, self.data['иммигранты'], 'bo-', label='Иммигранты')
        plt.plot(years, self.data['эмигранты'], 'ro-', label='Эмигранты')
        plt.xlabel('Год')
        plt.ylabel('Человек')
        plt.title('Миграция России')
        plt.legend()
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
        
        imm_forecast = self.moving_average_forecast(self.data['иммигранты'].values, n, window)
        em_forecast = self.moving_average_forecast(self.data['эмигранты'].values, n, window)
        
        print("\nПРОГНОЗ:")
        for i, y in enumerate(forecast_years):
            print(f"{y}: иммигранты {imm_forecast[i]:.0f}, эмигранты {em_forecast[i]:.0f}")
        
        plt.figure(figsize=(12,6))
        plt.plot(years, self.data['иммигранты'], 'bo-', label='Иммигранты (история)')
        plt.plot(years, self.data['эмигранты'], 'ro-', label='Эмигранты (история)')
        plt.plot(forecast_years, imm_forecast, 'b--o', label='Иммигранты (прогноз)')
        plt.plot(forecast_years, em_forecast, 'r--o', label='Эмигранты (прогноз)')
        plt.axvspan(forecast_years[0]-0.5, forecast_years[-1]+0.5, alpha=0.2, color='gray')
        plt.xlabel('Год')
        plt.ylabel('Человек')
        plt.title('Миграция с прогнозом')
        plt.legend()
        plt.grid(True)
        plt.show()
        input("Нажмите Enter...")
    
    def run(self):
        self.load_data()
        self.display_table()
        self.max_change_percent()
        self.plot_data()
        self.forecast()