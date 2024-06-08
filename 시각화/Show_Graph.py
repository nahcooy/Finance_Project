import pandas as pd
import FinanceDataReader as fdr
import plotly.graph_objects as go

def graph(stock_name):
    # CSV 파일에서 종목 정보를 읽어옴
    stock_codes = pd.read_csv('stock_codes.csv')

    # 주식 이름에 해당하는 종목 코드 조회
    stock_code = str(stock_codes[stock_codes['company'] == stock_name]['code'].values[0]).zfill(6)

    # 해당 주식의 상장일 가져오기
    listing_date = stock_codes[stock_codes['company'] == stock_name]['listing_date'].values[0]

    # FinanceDataReader를 사용하여 주식 데이터 가져오기
    df = fdr.DataReader(stock_code, start=listing_date, end=pd.Timestamp.today().strftime('%Y-%m-%d'))

    # 그래프로 시각화
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close', line_color='cyan'))

    fig.update_layout(
        title='{}의 주식 가격'.format(stock_name),
        xaxis_title='일자',
        yaxis_title='주식 가격',
        showlegend=True,
        legend=dict(x=0, y=1),
    )

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.show()

def main():
    stock_name = input("그래프로 보고싶은 주식 이름을 입력하세요: ")
    graph(stock_name)

if __name__=="__main__":
    main()