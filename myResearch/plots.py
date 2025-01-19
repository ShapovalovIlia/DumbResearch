import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных из Excel-файла
file_path = "final_data/academic1.xlsx"  # Укажи путь к своему Excel-файлу
data = pd.read_excel(file_path)

# Убедимся, что данные корректно считались
print(data.head())

# Построение графика
plt.figure(figsize=(10, 6))

# Отображение данных для boredom, interest, confusion, concentration
plt.plot(data['time'], data['boredom'], label='Boredom', marker='o')
plt.plot(data['time'], data['interest'], label='Interest', marker='o')
plt.plot(data['time'], data['confusion'], label='Confusion', marker='o')
plt.plot(data['time'], data['concentration'], label='Concentration', marker='o')

# Настройки графика
plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Dynamics of Boredom, Interest, Confusion, and Concentration Over Time')
plt.legend()
plt.grid(True)

# Показать график
plt.tight_layout()
plt.show()
