from math import floor, ceil

import matplotlib.pyplot as plt
import pandas as pd

dane = pd.read_csv('../data/dane.csv', sep=';', decimal=',', index_col=0)
dane['Sprzedaz całkowita'] = dane['prodA'] + dane['prodB']
sprzedaz = dane.drop(['prodA', 'prodB'], axis=1)

sprzedaz['mies_cat'] = pd.Categorical(sprzedaz.Miesiac,
                                      categories=["styczen", "luty", "marzec"],
                                      ordered=True)
sprzedaz.sort_values(['mies_cat', 'dzien'], inplace=True, ignore_index=True)

sprzedaz['date_str'] = sprzedaz['mies_cat'].astype(str) + ' ' + sprzedaz['dzien'].astype(str)

s_min = floor(sprzedaz['Sprzedaz całkowita'].min())
s_max = ceil(sprzedaz['Sprzedaz całkowita'].max())
s_half = s_min + (s_max - s_min) / 2
skala = [s_min, s_min + 2, s_half, s_max - 2, s_max]
s_etykiety = [f'{int(t)}k' for t in skala]

plt.xlabel('Dzien')
plt.ylabel('Sprzedaz całkowita')
plt.title('Sprzedaz całkowita')
plt.ylim(skala[0], skala[-1])

# x ticks
first_and_last_days = []
for month in sprzedaz['mies_cat'].unique():
    first_day = sprzedaz[sprzedaz['mies_cat'] == month].iloc[0]
    last_day = sprzedaz[sprzedaz['mies_cat'] == month].iloc[-1]

    first_and_last_days.append(first_day['date_str'])
    first_and_last_days.append(last_day['date_str'])

tick_positions = []
for date_str in first_and_last_days:
    tick_positions.append(sprzedaz[sprzedaz['date_str'] == date_str].index[0])

tick_labels = [sprzedaz.loc[pos, 'dzien'] for pos in tick_positions]
plt.xticks(tick_positions, tick_labels)

# y ticks
plt.yticks(skala, s_etykiety)
# plt.grid(axis='y', linestyle='--', alpha= 0.5)
plt.axhline(skala[1], linestyle='--', alpha=0.5, color='grey')
plt.axhline(skala[-2], linestyle='--', alpha=0.5, color='grey')

plt.plot(sprzedaz['date_str'], sprzedaz['Sprzedaz całkowita'])
plt.show()
