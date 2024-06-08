import pandas as pd
import os


def stock_code_crawling():
    stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0, encoding='cp949')[0]

    stock_code.sort_values(['상장일'], ascending=True, inplace=True)
    stock_code = stock_code[['회사명', '종목코드', '상장일']]
    stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code', '상장일': 'listing_date'})
    print(stock_code)

    return stock_code



def stock_name_checker(stockname, base_dir):
    csv_path = os.path.join(base_dir, 'stock_codes.csv')
    stock_codes = pd.read_csv(csv_path)
    return stockname in stock_codes['company'].values


def find_stock_code(stock_name, base_dir):
    csv_path = os.path.join(base_dir, 'stock_codes.csv')
    stock_codes = pd.read_csv(csv_path)
    code = stock_codes.loc[stock_codes['company'] == stock_name, 'code'].iloc[0]
    return code


def main():
    base_dir = './'  # 예시 기본 디렉토리 설정
    stock_code_crawling(base_dir)


if __name__ == "__main__":
    main()

