import pandas as pd
import matplotlib.pyplot as plt

#----------------------------1
df = pd.read_csv('Weather.csv')

#print(df.head())

#----------------------------2
num_records = len(df)
num_fields = len(df.columns)

print("к-кість записів:", num_records)
print("к-кість полів:", num_fields)
print("----------------------------")

#----------------------------3
M = 12
N = 300 * M

print("5 записів з {}-го:".format(M))
print(df.iloc[M:M+5])

print("\nкожен {}-ий запис:".format(N))
print(df.iloc[::N])

#----------------------------4
print("типи полів кожного запису:")
print(df.dtypes)

#----------------------------5
df['date'] = pd.to_datetime(df['CET']).dt.day
df['month'] = pd.to_datetime(df['CET']).dt.month
df['year'] = pd.to_datetime(df['CET']).dt.year

df.drop(columns=['CET'], inplace=True)
print(df.head())

#----------------------------6
print("----------------------------")
#--a) дні із порожнім значенням поля Events
print("к-кість днів із порожнім значенням поля Events:", df[' Events'].isna().sum())

#--б) день, у який середня вологість була мінімальною + швидкість вітру в цей день
min_humidity_day = df.loc[df[' Mean Humidity'].idxmin()]
print("день з найменшою середньою вологістю:", min_humidity_day['date'], min_humidity_day['month'], min_humidity_day['year'])
print("швидкість вітру в цей день:", min_humidity_day[' Mean Wind SpeedKm/h'])

#--с) місяці, коли середня температура [0; 5] градусів
months_with_temp_0_to_5 = df[(df['Mean TemperatureC'] >= 0) & (df['Mean TemperatureC'] <= 5)]['month'].unique()
print("місяці з середньою температурою від нуля до п’яти градусів:", months_with_temp_0_to_5)
print("----------------------------")

#----------------------------7
#--a) середня максимальна температура по кожному дню за всі роки
daily_max_temp_avg = df.groupby('date')['Max TemperatureC'].mean()
print("середня макс. температура по кожному дню за всі роки:")
print(daily_max_temp_avg)

#--б) к-кість днів у кожному році з туманом
foggy_days_per_year = df[df[' Events'].str.contains('Fog', na=False)].groupby(df['year'])[' Events'].count()
print("Кількість днів у кожному році з туманом:")
print(foggy_days_per_year)

#----------------------------8
events_count = df[' Events'].value_counts()

plt.figure(figsize=(10, 6))
events_count.plot(kind='bar')
plt.title('к-кість подій за весь період')
plt.xlabel('події')
plt.ylabel('к-кість')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#----------------------------9
direction_map = {0: 'north', 45: 'north-east', 90: 'east', 135: 'south-east', 180: 'south', 225: 'south-west', 270: 'west', 315: 'north-west'}
df['WindDirCompass'] = df['WindDirDegrees'].map(direction_map)

# Обчислення кількості випадків кожного з напрямків вітру
wind_direction_counts = df['WindDirCompass'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(wind_direction_counts, labels=wind_direction_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('кругова діаграма напрямків вітру')
plt.show()

#----------------------------10
avg_temp_dew = df.groupby(['month'])[['Max TemperatureC', 'Min DewpointC']].mean()

plt.figure(figsize=(12, 6))
#--a)
plt.bar(avg_temp_dew.index - 0.2, avg_temp_dew['Max TemperatureC'], width=0.4, label='середня макс. температура (°C)')
#--б)
plt.bar(avg_temp_dew.index + 0.2, avg_temp_dew['Min DewpointC'], width=0.4, label='середня мін. точка роси (°C)')

plt.title('ср. макс. температура та мін. точка роси по місяцях')
plt.xlabel('місяць')
plt.ylabel('ср. знач.')
plt.xticks(avg_temp_dew.index, ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'])
plt.legend()
plt.tight_layout()
plt.show()