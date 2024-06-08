import pandas as pd
import FinanceDataReader as fdr
import os


def save_all_stock_data_to_csv(stock_info, base_dir):
    print("stock_info 데이터프레임 내용 확인:")
    print(stock_info.head())

    listing_dates = stock_info['listing_date']
    stock_codes = stock_info['code']
    stock_names = stock_info['company']

    for ld, sc, sn in zip(listing_dates, stock_codes, stock_names):
        sc = '{:06d}'.format(sc)
        try:
            df = fdr.DataReader(str(sc), start=ld, end=pd.Timestamp.today().strftime('%Y-%m-%d'))
            df = df.reset_index()
            csv_filename = os.path.join(base_dir, 'stock_investing_gui', 'stock_data', 'day', f'{sn}_day.csv')
            df.to_csv(csv_filename, index=False)
            print(f'{csv_filename} 파일이 저장되었습니다.')
        except Exception as e:
            print(f'주식 데이터를 저장하는 동안 오류가 발생했습니다: {e}')

def main():
    base_dir = './'  # 예시 기본 디렉토리 설정
    stock_info = pd.read_csv(os.path.join(base_dir, 'stock_codes.csv'))
    save_all_stock_data_to_csv(stock_info, base_dir)

if __name__ == "__main__":
    main()
