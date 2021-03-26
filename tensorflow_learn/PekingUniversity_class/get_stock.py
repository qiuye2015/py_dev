import tushare as ts

code = '600519'
df1 = ts.get_k_data(code, ktype='D', start='2010-04-26', end='2020-04-26')
dataPath1 = './SH' + code + '.csv'  # ./SH600519.csv
df1.to_csv(dataPath1)
