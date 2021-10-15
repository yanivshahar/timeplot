import json
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from datetime import datetime

with open('portfolio.json') as f:
    portfolio = json.load(f)

START_DATE = '2017-01-01'
START_DATE = datetime.strptime(START_DATE, '%Y-%m-%d')

historical = pdr.yahoo.daily.YahooDailyReader(symbols=list(portfolio.keys()), start=START_DATE)
historical = historical.read().Close
historical['Value'] = sum([portfolio[symbol]*historical[symbol] for symbol in portfolio.keys()])

init_investment = historical.iloc[0].Value

benchmark_symbol = 'VOO'
benchmark = pdr.yahoo.daily.YahooDailyReader(symbols=benchmark_symbol, start=START_DATE)
benchmark = benchmark.read().Close

frac_bench_amount = init_investment / benchmark.iloc[0]
benchmark_values = benchmark * frac_bench_amount

fig, ax = plt.subplots(figsize=(12,8))
ax.plot(historical.Value, label='Portfolio')
ax.plot(benchmark_values, label='Benchmark')

ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%Y'))
ax.xaxis.set_major_locator(mpl.dates.YearLocator(1))
ax.xaxis.set_minor_locator(mpl.dates.MonthLocator())
ax.xaxis.set_tick_params(labelbottom=True)
ax.yaxis.set_major_formatter('{x:1.0f}$')
ax.tick_params(axis='x', labelrotation=45, labelsize=14)
ax.tick_params(axis='y', labelsize=14)

fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95), fontsize=16)
fig.patch.set_facecolor('white')
fig.tight_layout()
fig.savefig('benchmark.png')
