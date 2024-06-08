import pandas as pd
import matplotlib.pyplot as plt
import os

def find_nearest_date(data, target_date):
    return data[data['Date'] <= target_date]['Date'].max()

def stock_info_Visualization(base_dir, stock_name, start_date, end_date, selected_subdirs):
    num_subdirs = len(selected_subdirs)
    if num_subdirs == 1:
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
        axes = [axes]  # Make axes a list for consistent indexing
    else:
        fig, axes = plt.subplots(nrows=num_subdirs, ncols=1, figsize=(10, 5 * num_subdirs))

    day_filtered = None  # Initialize day_filtered to avoid UnboundLocalError

    if 'BB' in selected_subdirs:
        bb_data = pd.read_csv(os.path.join(base_dir, f'stock_investing_gui/stock_data/BB/{stock_name}_BB.csv'))
    if 'day' in selected_subdirs or any(subdir in selected_subdirs for subdir in ['ma', 'RSI', 'macd', 'week', 'month']):
        day_data = pd.read_csv(os.path.join(base_dir, f'stock_investing_gui/stock_data/day/{stock_name}_day.csv'))
        day_filtered = day_data[(day_data['Date'] >= start_date) & (day_data['Date'] <= end_date)]  # Define day_filtered here
    if 'ma' in selected_subdirs:
        ma_data = pd.read_csv(os.path.join(base_dir, f'stock_investing_gui/stock_data/ma/{stock_name}_ma.csv'))
    if 'RSI' in selected_subdirs:
        rsi_data = pd.read_csv(os.path.join(base_dir, f'stock_investing_gui/stock_data/RSI/{stock_name}_RSI.csv'))
    if 'macd' in selected_subdirs:
        macd_data = pd.read_csv(os.path.join(base_dir, f'stock_investing_gui/stock_data/macd/{stock_name}_macd.csv'))
    if 'week' in selected_subdirs:
        week_data = pd.read_csv(os.path.join(base_dir, f'stock_investing_gui/stock_data/week/{stock_name}_week.csv'))
    if 'month' in selected_subdirs:
        month_data = pd.read_csv(os.path.join(base_dir, f'stock_investing_gui/stock_data/month/{stock_name}_month.csv'))

    try:
        start_date_y = day_data.loc[day_data['Date'] == start_date].index[0]
        end_date_y = day_data.loc[day_data['Date'] == end_date].index[0]
    except IndexError:
        print(f"Error: One of the dates ({start_date} or {end_date}) not found in day_data.")
        return

    for i, subdir in enumerate(selected_subdirs):
        if subdir == 'BB':
            bb_filtered = bb_data[(bb_data['Date'] >= start_date) & (bb_data['Date'] <= day_data.iloc[end_date_y]['Date'])]
            day_filtered = day_data[(day_data['Date'] >= start_date) & (day_data['Date'] <= day_data.iloc[end_date_y]['Date'])]
            axes[i].plot(day_filtered['Date'], day_filtered['Close'], label='Close Price')
            axes[i].plot(bb_filtered['Date'], bb_filtered['Upper_Band'], label='Upper Bollinger Band', linestyle='--')
            axes[i].plot(bb_filtered['Date'], bb_filtered['Lower_Band'], label='Lower Bollinger Band', linestyle='--')
            axes[i].set_title('Stock Price with Bollinger Bands')
            axes[i].set_ylabel('Price')
            axes[i].legend()
            axes[i].grid(True)

        if subdir == 'day':
            day_filtered = day_data[(day_data['Date'] >= start_date) & (day_data['Date'] <= end_date)]
            axes[i].plot(day_filtered['Date'], day_filtered['Close'], label='Close Price')
            axes[i].set_title('Daily Prices')
            axes[i].set_ylabel('Price')
            axes[i].legend()
            axes[i].grid(True)

        if subdir == 'ma':
            ma_filtered = ma_data[(ma_data['Date'] >= start_date) & (ma_data['Date'] <= day_data.iloc[end_date_y]['Date'])]
            axes[i].plot(day_filtered['Date'], day_filtered['Close'], label='Close Price')
            for col in ma_filtered.columns[1:]:
                axes[i].plot(ma_filtered['Date'], ma_filtered[col], label=col, linewidth=0.75)
            axes[i].set_title('Moving Averages')
            axes[i].set_ylabel('Price')
            axes[i].legend()
            axes[i].grid(True)

        if subdir == 'RSI':
            rsi_filtered = rsi_data[(rsi_data['Date'] >= start_date) & (rsi_data['Date'] <= day_data.iloc[end_date_y]['Date'])]
            axes[i].plot(rsi_filtered['Date'], rsi_filtered['RSI'], label='RSI')
            axes[i].axhline(y=70, color='r', linestyle='--', label='Overbought')
            axes[i].axhline(y=30, color='g', linestyle='--', label='Oversold')
            axes[i].set_title('Relative Strength Index (RSI)')
            axes[i].set_xlabel('Date')
            axes[i].set_ylabel('RSI')
            axes[i].legend()
            axes[i].grid(True)

        if subdir == 'macd':
            macd_filtered = macd_data[(macd_data['Date'] >= start_date) & (macd_data['Date'] <= day_data.iloc[end_date_y]['Date'])]
            axes[i].plot(macd_filtered['Date'], macd_filtered['macd'], label='MACD')
            axes[i].plot(macd_filtered['Date'], macd_filtered['signal'], label='Signal')
            axes[i].bar(macd_filtered['Date'], macd_filtered['histogram'], label='Histogram', color='gray', alpha=0.3)
            axes[i].axhline(y=0, color='r', linestyle='--', label='Zero Line')
            axes[i].set_title('MACD')
            axes[i].set_xlabel('Date')
            axes[i].set_ylabel('Value')
            axes[i].legend()
            axes[i].grid(True)

        # if subdir == 'week':
        #     week_filtered = week_data[(week_data['Date'] >= start_date) & (week_data['Date'] <= day_data.iloc[end_date_y]['Date'])]
        #     axes[i].plot(week_filtered['Date'], week_filtered['Close'], label='Close Price')
        #     axes[i].set_title('Weekly Prices')
        #     axes[i].set_ylabel('Price')
        #     axes[i].legend()
        #     axes[i].grid(True)
        #
        # if subdir == 'month':
        #     month_filtered = month_data[(month_data['Date'] >= start_date) & (month_data['Date'] <= day_data.iloc[end_date_y]['Date'])]
        #     axes[i].plot(month_filtered['Date'], month_filtered['Close'], label='Close Price')
        #     axes[i].set_title('Monthly Prices')
        #     axes[i].set_ylabel('Price')
        #     axes[i].legend()
        #     axes[i].grid(True)

        if day_filtered is not None:
            num_indices = 10
            index_step = len(day_filtered) // num_indices
            x_ticks_indices = [i for i in range(0, len(day_filtered), index_step)]
            x_tick_labels = [day_filtered.iloc[i]['Date'] for i in x_ticks_indices]

            axes[i].set_xticks(x_ticks_indices)
            axes[i].set_xticklabels(x_tick_labels, rotation=45, ha='right')

            start_date = day_filtered.iloc[0]['Date']
            end_date = day_filtered.iloc[index_step]['Date']

    plt.tight_layout()
    return fig
