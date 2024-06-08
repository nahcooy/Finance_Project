import pandas as pd
import matplotlib.pyplot as plt
import os


def find_macd_cross_dates(directory='../stock_data/macd/'):
    results = {}
    # 지정된 디렉터리에서 모든 CSV 파일을 찾아 처리
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            stock_name = filename.split('_')[0]  # 파일 이름에서 주식 이름 추출
            filepath = os.path.join(directory, filename)
            try:
                data = pd.read_csv(filepath)
                if 'Date' in data.columns and 'macd' in data.columns:
                    # MACD가 0을 돌파하는 날짜 찾기
                    crosses = data[(data['macd'].shift(1) < 0) & (data['macd'] > 0)]
                    if not crosses.empty:
                        # 결과 딕셔너리에 주식 이름과 돌파 날짜 목록 저장
                        results[stock_name] = crosses['Date'].tolist()
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue

    # 결과 딕셔너리를 데이터프레임으로 변환하여 CSV 파일로 저장
    cross_dates = []
    for stock, dates in results.items():
        for date in dates:
            cross_dates.append({'Stock': stock, 'Date': date})
    df = pd.DataFrame(cross_dates)
    df.to_csv('macd_cross_dates.csv', index=False)

    return


def calculate_growth_rate(start_price, end_price):
    return (end_price - start_price) / start_price * 100

def calculate_growth_rate(start_price, end_price):
    """ 주어진 시작 가격과 종료 가격에서 성장률 계산 """
    return (end_price - start_price) / start_price * 100

def evaluate_stock_growth(cross_dates_file, day_directory='../stock_data/day/'):
    # MACD 상향 돌파 날짜를 포함한 CSV 파일 읽기
    df_cross_dates = pd.read_csv(cross_dates_file)
    ideal_dates_list = []  # 주식과 날짜의 쌍을 저장할 리스트

    # 각 주식의 상향 돌파 날짜에 대해 세분화된 상승률 계산
    for index, row in df_cross_dates.iterrows():
        stock_name = row['Stock']
        cross_date = row['Date']
        day_filepath = os.path.join(day_directory, f'{stock_name}_day.csv')

        try:
            day_data = pd.read_csv(day_filepath)
            # 상향 돌파 날짜에 해당하는 인덱스 찾기
            idx = day_data[day_data['Date'] == cross_date].index.item()
            # 60 거래일 전 인덱스 계산
            start_idx = max(0, idx - 60)

            if start_idx == 0 or idx - start_idx < 60:
                continue  # 충분한 데이터가 없을 경우 건너뜀

            consistent_growth = True
            # 각 20일 단위로 상승률 검증
            for i in range(start_idx, idx, 20):
                if i + 19 < len(day_data):
                    start_price = day_data.iloc[i]['Close']
                    end_price = day_data.iloc[i + 19]['Close']
                    if calculate_growth_rate(start_price, end_price) < 3:
                        consistent_growth = False
                        break

            if consistent_growth:
                ideal_dates_list.append({'Stock': stock_name, 'Date': cross_date})
                print(index, row['Stock'], row['Date'])

        except Exception as e:
            print(f"Error processing day data for {stock_name}: {e}")
            continue

    # 결과를 DataFrame으로 변환 후 CSV로 저장
    df_results = pd.DataFrame(ideal_dates_list)
    df_results.to_csv('Ideal_growth_dates.csv', index=False)
    print("Saved ideal growth dates to Ideal_growth_dates.csv")

def main():
    # find_macd_cross_dates()
    evaluate_stock_growth('macd_cross_dates.csv')

if __name__ == "__main__":
    main()
