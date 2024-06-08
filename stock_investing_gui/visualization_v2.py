import pandas as pd
import matplotlib.pyplot as plt
import os

def find_nearest_date(data, target_date):
    # 데이터프레임에서 target_date와 가장 가까운 이전 날짜를 찾아 반환
    data['Date'] = pd.to_datetime(data['Date'])  # Date 열을 Timestamp 형식으로 변환
    return data[data['Date'] <= target_date]['Date'].max()

def stock_info_Visualization_v2(stock_name, buy_date, sell_date, period_x, period_y, base_dir):
    # 데이터 불러오기
    bb_data = pd.read_csv(f'{base_dir}/stock_investing_gui/stock_data/BB/{stock_name}_BB.csv')
    day_data = pd.read_csv(f'{base_dir}/stock_investing_gui/stock_data/day/{stock_name}_day.csv')
    ma_data = pd.read_csv(f'{base_dir}/stock_investing_gui/stock_data/ma/{stock_name}_ma.csv')
    rsi_data = pd.read_csv(f'{base_dir}/stock_investing_gui/stock_data/RSI/{stock_name}_RSI.csv')
    macd_data = pd.read_csv(f'{base_dir}/stock_investing_gui/stock_data/macd/{stock_name}_macd.csv')  # MACD 데이터 불러오기

    # Date 열을 Timestamp 형식으로 변환
    day_data['Date'] = pd.to_datetime(day_data['Date'])
    bb_data['Date'] = pd.to_datetime(bb_data['Date'])
    ma_data['Date'] = pd.to_datetime(ma_data['Date'])
    rsi_data['Date'] = pd.to_datetime(rsi_data['Date'])
    macd_data['Date'] = pd.to_datetime(macd_data['Date'])

    # 시작 날짜와 종료 날짜 설정
    start_date_x = find_nearest_date(day_data, pd.to_datetime(buy_date) - pd.Timedelta(days=period_x))
    end_date_y = find_nearest_date(day_data, pd.to_datetime(sell_date) + pd.Timedelta(days=period_y))

    # 데이터 필터링
    bb_filtered = bb_data[(bb_data['Date'] >= start_date_x) & (bb_data['Date'] <= end_date_y)]
    day_filtered = day_data[(day_data['Date'] >= start_date_x) & (day_data['Date'] <= end_date_y)]
    ma_filtered = ma_data[(ma_data['Date'] >= start_date_x) & (ma_data['Date'] <= end_date_y)]
    rsi_filtered = rsi_data[(rsi_data['Date'] >= start_date_x) & (rsi_data['Date'] <= end_date_y)]
    macd_filtered = macd_data[(macd_data['Date'] >= start_date_x) & (macd_data['Date'] <= end_date_y)]

    # 시각화
    fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(10, 25))

    # 종가 및 볼린저 밴드 시각화
    axes[0].plot(day_filtered['Date'], day_filtered['Close'], label='Close Price')
    axes[0].plot(bb_filtered['Date'], bb_filtered['Upper_Band'], label='Upper Bollinger Band', linestyle='--')
    axes[0].plot(bb_filtered['Date'], bb_filtered['Lower_Band'], label='Lower Bollinger Band', linestyle='--')
    axes[0].set_title('Stock Price with Bollinger Bands')
    axes[0].set_ylabel('Price')
    axes[0].legend()
    axes[0].grid(True)

    # 이동평균 시각화
    axes[1].plot(day_filtered['Date'], day_filtered['Close'], label='Close Price')
    for col in ma_filtered.columns[1:]:
        axes[1].plot(ma_filtered['Date'], ma_filtered[col], label=col, linewidth=0.75)
    axes[1].set_title('Moving Averages')
    axes[1].set_ylabel('Price')
    axes[1].legend()
    axes[1].grid(True)

    # RSI 시각화
    axes[2].plot(rsi_filtered['Date'], rsi_filtered['RSI'], label='RSI')
    axes[2].axhline(y=70, color='r', linestyle='--', label='Overbought')
    axes[2].axhline(y=30, color='g', linestyle='--', label='Oversold')
    axes[2].set_title('Relative Strength Index (RSI)')
    axes[2].set_xlabel('Date')
    axes[2].set_ylabel('RSI')
    axes[2].legend()
    axes[2].grid(True)

    # MACD 시각화
    axes[3].plot(macd_filtered['Date'], macd_filtered['macd'], label='MACD')
    axes[3].plot(macd_filtered['Date'], macd_filtered['signal'], label='Signal', linestyle='--')
    axes[3].bar(macd_filtered['Date'], macd_filtered['histogram'], label='Histogram', color='grey', alpha=0.5)
    axes[3].set_title('MACD')
    axes[3].set_xlabel('Date')
    axes[3].set_ylabel('Value')
    axes[3].legend()
    axes[3].grid(True)

    # 종가 및 거래량 시각화
    axes[4].plot(day_filtered['Date'], day_filtered['Close'], label='Close Price', color='blue')
    axes_volume = axes[4].twinx()  # 두 번째 y축 생성
    axes_volume.bar(day_filtered['Date'], day_filtered['Volume'], label='Volume', color='green', alpha=0.5)
    axes[4].set_title('Stock Price and Volume')
    axes[4].set_xlabel('Date')
    axes[4].set_ylabel('Price')
    axes_volume.set_ylabel('Volume')
    axes[4].legend(loc='upper left')
    axes_volume.legend(loc='upper right')

    # 인덱스 선택
    num_indices = 10
    index_step = max(len(day_filtered) // num_indices, 1)  # Ensure index_step is at least 1
    x_ticks_indices = [i for i in range(0, len(day_filtered), index_step)]
    x_tick_labels = [day_filtered.iloc[i]['Date'] for i in x_ticks_indices]

    for ax in axes:
        # x축 눈금과 라벨 설정
        ax.set_xticks(x_ticks_indices)
        ax.set_xticklabels(x_tick_labels, rotation=45, ha='right')  # 눈금 라벨을 45도 기울여서 우측 정렬

        # 선택한 기간에 대한 범위를 axvspan 함수에 전달
        ax.axvspan(pd.to_datetime(buy_date), pd.to_datetime(sell_date), color='gray', alpha=0.075)

        ax.axvline(pd.to_datetime(buy_date), color='black', linestyle='--', label='Buy Date')

    plt.tight_layout()
    save_directory = os.path.join(base_dir, 'stock_investing_gui', stock_name)
    os.makedirs(save_directory, exist_ok=True)

    # 이미지 파일 경로
    save_path = os.path.join(save_directory, f'{stock_name}_{buy_date}_{sell_date}_visualization.png')

    # 이미지 파일로 저장
    plt.savefig(save_path)

    return save_path

def main():
    stock_info_Visualization_v2(stock_name='힘스', buy_date='2023-01-02', sell_date='2023-03-01', period_x=20, period_y=20, base_dir='.')

if __name__ == "__main__":
    main()
