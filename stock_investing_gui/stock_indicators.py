import pandas as pd
import glob
import os


def calculate_bollinger_bands(data, period=20, num_std=2):
    ma = data.rolling(window=period).mean()
    std = data.rolling(window=period).std()
    upper_band = ma + (num_std * std)
    lower_band = ma - (num_std * std)
    return upper_band, lower_band


def bollinger_bands_for_all(base_dir, period=20, num_std=2):
    directory_path = os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'day')
    csv_files = glob.glob(f'{directory_path}/*.csv')
    for csv_file in csv_files:
        stock_name = os.path.splitext(os.path.basename(csv_file))[0][:-4]
        df = pd.read_csv(csv_file)
        price_data = pd.Series(df['Close'])
        date_data = pd.Series(df['Date'])
        upper_band, lower_band = calculate_bollinger_bands(price_data)
        df = pd.DataFrame({'Date': date_data, 'Close': price_data, 'Upper_Band': upper_band, 'Lower_Band': lower_band})
        output_path = os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'BB')
        os.makedirs(output_path, exist_ok=True)
        df.to_csv(f'{output_path}/{stock_name}_BB.csv', index=False)


def day2weekNmonth(base_dir, stock_name):
    df = pd.read_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'day', f'{stock_name}_day.csv'))
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    weekly_data = df.resample('W').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum', 'Change': 'sum'})
    weekly_data.to_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'week', f'{stock_name}_week.csv'))
    monthly_data = df.resample('ME').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum', 'Change': 'sum'})
    monthly_data.to_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'month', f'{stock_name}_month.csv'))



def all_stock_data_day2weekNmonth(base_dir):
    directory_path = os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'day')
    csv_files = glob.glob(f'{directory_path}/*.csv')
    for csv_file in csv_files:
        stock_name = os.path.splitext(os.path.basename(csv_file))[0][:-4]
        day2weekNmonth(base_dir, stock_name)



def caculate_moving_average(df, period):
    return df.rolling(window=period).mean()


def create_moving_average(base_dir, stock_name, period):
    df = pd.read_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'day', f'{stock_name}_day.csv'))
    price_data = pd.Series(df['Close'])
    moving_average = caculate_moving_average(price_data, period)
    try:
        macd_csv = pd.read_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'special', f'{stock_name}_ma.csv'))
    except FileNotFoundError:
        create_basic_moving_average(base_dir, stock_name)
        macd_csv = pd.read_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'special', f'{stock_name}_ma.csv'))
    macd_csv[f'ma_{period:03d}'] = moving_average
    macd_csv.to_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'special', f'{stock_name}_ma_{period:03d}.csv'), index=False)


def create_basic_moving_average(base_dir, stock_name):
    df = pd.read_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'day', f'{stock_name}_day.csv'))
    price_data = pd.Series(df['Close'])
    date_data = pd.Series(df['Date'])
    periods = [5, 10, 20, 60, 120, 240]
    ma_data = {f'ma_{period:03d}': caculate_moving_average(price_data, period) for period in periods}
    df_ma = pd.DataFrame({'Date': date_data, **ma_data})
    df_ma.to_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'ma', f'{stock_name}_ma.csv'), index=False)


def ma4all(base_dir):
    directory_path = os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'day')
    csv_files = glob.glob(f'{directory_path}/*.csv')
    for csv_file in csv_files:
        stock_name = os.path.splitext(os.path.basename(csv_file))[0][:-4]
        create_basic_moving_average(base_dir, stock_name)


def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    short_ema = data.ewm(span=short_period, adjust=False).mean()
    long_ema = data.ewm(span=long_period, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_histogram = macd_line - signal_line
    return macd_line, signal_line, macd_histogram


def create_macd_data(base_dir, stock_name):
    df = pd.read_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'day', f'{stock_name}_day.csv'))
    price_data = pd.Series(df['Close'])
    date_data = pd.Series(df['Date'])
    macd, signal, histogram = calculate_macd(price_data)
    df_macd = pd.DataFrame({'Date': date_data, 'macd': macd, 'signal': signal, 'histogram': histogram})
    df_macd.to_csv(os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'macd', f'{stock_name}_macd.csv'), index=False)


def create_all_macd(base_dir):
    directory_path = os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'day')
    csv_files = glob.glob(f'{directory_path}/*.csv')
    for csv_file in csv_files:
        stock_name = os.path.splitext(os.path.basename(csv_file))[0][:-4]
        create_macd_data(base_dir, stock_name)


def calculate_rsi(df, rsi_period=14):
    df['Price Change'] = df['Change']
    df['Gain'] = df['Change'].apply(lambda x: x if x > 0 else 0)
    df['Loss'] = df['Change'].apply(lambda x: abs(x) if x < 0 else 0)
    df['Avg Gain'] = df['Gain'].rolling(window=rsi_period).mean()
    df['Avg Loss'] = df['Loss'].rolling(window=rsi_period).mean()
    df['RS'] = df['Avg Gain'] / df['Avg Loss']
    df['RSI'] = 100 - (100 / (1 + df['RS']))
    return df


def create_rsi_all_csv(base_dir, rsi_period=14):
    directory_path = os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'day')
    csv_files = glob.glob(f'{directory_path}/*.csv')
    for csv_file in csv_files:
        stock_name = os.path.splitext(os.path.basename(csv_file))[0][:-4]
        df = pd.read_csv(csv_file)
        df = calculate_rsi(df, rsi_period)
        df = df[['Date', 'Avg Gain', 'Avg Loss', 'RS', 'RSI']]
        output_path = os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'RSI')
        os.makedirs(output_path, exist_ok=True)
        df.to_csv(f'{output_path}/{stock_name}_RSI.csv', index=False)
