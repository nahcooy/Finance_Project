import pandas as pd


def simulate_investment(stock_file, macd_directory, day_directory):
    # 매수해야 할 주식과 날짜 읽기
    df_stocks = pd.read_csv(stock_file)

    results = []

    for index, row in df_stocks.iterrows():
        stock_name = row['Stock']
        buy_date = row['Date']
        macd_file_path = f'{macd_directory}/{stock_name}_macd.csv'
        day_file_path = f'{day_directory}/{stock_name}_day.csv'

        try:
            # MACD 데이터와 주가 데이터 읽기
            df_macd = pd.read_csv(macd_file_path)
            df_day = pd.read_csv(day_file_path)

            # 매수 날짜의 데이터 추출
            buy_idx = df_day[df_day['Date'] == buy_date].index.item()
            buy_price = df_day.iloc[buy_idx]['Close']

            # 매도 조건 탐색
            duration = 0
            for i in range(buy_idx + 1, len(df_day)):
                duration += 1
                current_price = df_day.iloc[i]['Open']
                signal = df_macd.iloc[i]['signal']
                macd = df_macd.iloc[i]['macd']

                # 매도 조건 확인
                if (current_price < buy_price * 0.93) or (0 > signal) or (current_price > buy_price * 1.5):
                    sell_price = current_price
                    break
            else:
                # 매도 조건이 충족되지 않을 경우 현재 가격 사용
                sell_price = df_day.iloc[-1]['Close']

            # 수익률 계산
            return_rate = (sell_price - buy_price) / buy_price * 100
            results.append(
                {'Stock': stock_name, 'Buy Date': buy_date, 'Duration': duration, 'Sell Price': sell_price, 'Return Rate': return_rate})
            print(stock_name, buy_date, buy_price, sell_price, return_rate)
        except Exception as e:
            print(f"Error processing data for {stock_name} {buy_date}: {e}")

    # 결과를 DataFrame으로 저장
    df_results = pd.DataFrame(results)
    df_results.to_csv('investment_simulation_results.csv', index=False)
    print("Simulation results saved to investment_simulation_results.csv")


# 파일 경로에 따라 경로를 설정하세요.
simulate_investment('Ideal_growth_dates.csv', '../stock_data/macd/', '../stock_data/day/')