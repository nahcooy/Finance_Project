import pandas as pd
import os

def simulate_investment(macd_directory, day_directory, base_dir, stock_name):
    results = []
    macd_file_path = f'{macd_directory}/{stock_name}_macd.csv'
    day_file_path = f'{day_directory}/{stock_name}_day.csv'
    return_rate = None

    try:
        # MACD 데이터와 주가 데이터 읽기
        df_macd = pd.read_csv(macd_file_path)
        df_day = pd.read_csv(day_file_path)

        # 매수 조건: MACD가 0을 -에서 +로 돌파할 때 매수
        for buy_idx in range(31, len(df_macd)):  # 첫 번째 행은 이전 값이 없으므로 1부터 시작
            if df_macd.iloc[buy_idx - 1]['macd'] < 0 and df_macd.iloc[buy_idx]['macd'] > 0:
                buy_date = df_day.iloc[buy_idx]['Date']
                buy_price = df_day.iloc[buy_idx]['Close']

                # 매도 조건 탐색
                duration = 0
                for i in range(buy_idx + 1, len(df_day)):
                    duration += 1
                    current_price = df_day.iloc[i]['Open']
                    signal = df_macd.iloc[i]['signal']
                    macd = df_macd.iloc[i]['macd']

                    # 매도 조건 확인
                    if (current_price < buy_price * 0.93) or (signal > 0 and df_macd.iloc[i-1]['signal'] <= 0) or (current_price > buy_price * 1.5):
                        sell_price = current_price
                        sell_date = df_day.iloc[i]['Date']
                        break
                else:
                    # 매도 조건이 충족되지 않을 경우 현재 가격 사용
                    sell_price = df_day.iloc[-1]['Close']
                    sell_date = df_day.iloc[-1]['Date']

                # 수익률 계산
                return_rate = round((sell_price - buy_price) / buy_price * 100, 4)
                results.append(
                    {'Stock': stock_name, 'Buy Date': buy_date, 'Buy Price': buy_price, 'Sell Date': sell_date, 'Sell Price': sell_price,
                     'Return Rate': return_rate})
                print(stock_name, buy_date, buy_price, sell_date, sell_price, return_rate)
    except FileNotFoundError as e:
        print(f"Error: File not found for {stock_name}: {e}")
        return None
    except Exception as e:
        print(f"Error processing data for {stock_name}: {e}")
        return None

    # 결과를 DataFrame으로 저장
    save_directory = os.path.join(base_dir, 'stock_investing_gui', stock_name)
    os.makedirs(save_directory, exist_ok=True)
    save_path = os.path.join(save_directory, f'investment_simulation_results_{stock_name}.csv')
    df_results = pd.DataFrame(results)
    df_results.to_csv(save_path, index=False)
    print(f"Simulation results saved to {save_path}")

    return return_rate
