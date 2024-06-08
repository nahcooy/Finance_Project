import PySimpleGUI as sg
import pandas as pd
import os
import matplotlib as plt

def stock_info_Visualization(stock_name, start_date, period_x, period_y):
    # 데이터 불러오기
    bb_data = pd.read_csv(f'../stock_data/BB/{stock_name}_BB.csv')
    day_data = pd.read_csv(f'../stock_data/day/{stock_name}_day.csv')
    ma_data = pd.read_csv(f'../stock_data/ma/{stock_name}_ma.csv')
    rsi_data = pd.read_csv(f'../stock_data/RSI/{stock_name}_RSI.csv')

    # 시작 날짜를 기준으로 이전의 날짜들을 찾음
    start_date_x = start_date
    start_date_y = day_data.loc[day_data['Date'] == start_date_x].index[0] + period_x
    end_date_y = start_date_y + period_y

    # 데이터 필터링
    bb_filtered = bb_data[(bb_data['Date'] >= start_date_x) & (bb_data['Date'] <= day_data.iloc[end_date_y]['Date'])]
    day_filtered = day_data[(day_data['Date'] >= start_date_x) & (day_data['Date'] <= day_data.iloc[end_date_y]['Date'])]
    ma_filtered = ma_data[(ma_data['Date'] >= start_date_x) & (ma_data['Date'] <= day_data.iloc[end_date_y]['Date'])]
    rsi_filtered = rsi_data[(rsi_data['Date'] >= start_date_x) & (rsi_data['Date'] <= day_data.iloc[end_date_y]['Date'])]

    # 시각화
    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 20))

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

    # 종가 및 거래량 시각화
    axes[3].plot(day_filtered['Date'], day_filtered['Close'], label='Close Price', color='blue')
    axes_volume = axes[3].twinx()  # 두 번째 y축 생성
    axes_volume.bar(day_filtered['Date'], day_filtered['Volume'], label='Volume', color='green', alpha=0.5)
    axes[3].set_title('Stock Price and Volume')
    axes[3].set_xlabel('Date')
    axes[3].set_ylabel('Price')
    axes_volume.set_ylabel('Volume')
    axes[3].legend(loc='upper left')
    axes_volume.legend(loc='upper right')

    # 인덱스 선택
    num_indices = 10
    index_step = len(day_filtered) // num_indices
    x_ticks_indices = [i for i in range(0, len(day_filtered), index_step)]
    x_tick_labels = [day_filtered.iloc[i]['Date'] for i in x_ticks_indices]

    for ax in axes:
        # x축 눈금과 라벨 설정
        ax.set_xticks(x_ticks_indices)
        ax.set_xticklabels(x_tick_labels, rotation=45, ha='right')  # 눈금 라벨을 45도 기울여서 우측 정렬

        # 인덱스를 사용하여 특정 기간 선택
        start_date = day_filtered.iloc[0]['Date']
        end_date = day_filtered.iloc[period_x]['Date']

        # 선택한 기간에 대한 범위를 axvspan 함수에 전달
        ax.axvspan(start_date, end_date, color='gray', alpha=0.075)

        ax.axvline(day_filtered['Date'][start_date_y], color='black', linestyle='--', label=f'Period Y: {period_y}')

    plt.tight_layout()
    save_directory = './vis/vis-1'
    os.makedirs(save_directory, exist_ok=True)

    # 이미지 파일 경로
    save_path = os.path.join(save_directory, f'{stock_name}_{start_date}_{period_x}_{period_y}_visualization.png')

    # 이미지 파일로 저장
    plt.savefig(save_path)
    plt.show()

    return

def main():
    # 필요한 데이터 파일 로드하여 날짜 콤보박스에 사용
    day_data_path = '../stock_data/day/힘스_day.csv'
    day_data = pd.read_csv(day_data_path)
    available_dates = list(day_data['Date'])

    # GUI 레이아웃 설정
    layout = [
        [sg.Text('Stock Name'), sg.InputText(key='stock_name')],
        [sg.Text('Start Date'), sg.Combo(available_dates, default_value=available_dates[0], key='start_date')],
        [sg.Text('Period X'), sg.InputText(key='period_x')],
        [sg.Text('Period Y'), sg.InputText(key='period_y')],
        [sg.Button('Visualize'), sg.Button('Exit')]
    ]

    # 창 생성
    window = sg.Window('Stock Info Visualization', layout)

    # 이벤트 루프
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == 'Visualize':
            stock_name = values['stock_name']
            start_date = values['start_date']
            try:
                period_x = int(values['period_x'])
                period_y = int(values['period_y'])

                stock_info_Visualization(stock_name, start_date, period_x, period_y)
            except ValueError:
                sg.popup_error('Invalid input for Period X or Period Y. Please enter valid numbers.')

    window.close()

if __name__=="__main__":
    main()