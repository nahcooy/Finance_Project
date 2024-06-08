# 주식 투자 도구

이 프로젝트는 주식 데이터를 크롤링, 분석 및 시각화하기 위한 종합적인 주식 투자 도구입니다. `stock_investing_gui.py` 메인 스크립트는 PySimpleGUI를 사용하여 그래픽 사용자 인터페이스(GUI)를 제공하며, 다른 스크립트는 주식 데이터 크롤링, 지표 계산 및 데이터 시각화와 같은 다양한 작업을 처리합니다.

## 목차

1. [설치](#설치)
2. [사용법](#사용법)
3. [파일 설명](#파일-설명)
    - [stock_investing_gui.py](#stock_investing_guipy)
    - [Listed_Stock_Data_Crawling.py](#listed_stock_data_crawlingpy)
    - [Save_All_Stock_Data.py](#save_all_stock_datapy)
    - [investment_simulator.py](#investment_simulatorpy)
    - [stock_indicators.py](#stock_indicatorspy)
    - [visualization_functions.py](#visualization_functionspy)
    - [visualization_v2.py](#visualization_v2py)

## 설치

1. 프로젝트를 클론합니다:
    ```sh
    git clone https://github.com/your-repository/stock-investing-tool.git
    ```

2. 필요한 패키지를 설치합니다:
    ```sh
    pip install -r requirements.txt
    ```

## 사용법

1. `stock_investing_gui.py` 스크립트를 실행하여 GUI를 엽니다:
    ```sh
    python stock_investing_gui.py
    ```

2. GUI에서 다음 옵션을 선택할 수 있습니다:
    - **Set Base Dir**: 기본 디렉토리를 설정합니다.
    - **Crawl Stock Data**: 주식 데이터를 크롤링합니다.
    - **Visualize Stock Data**: 주식 데이터를 시각화합니다.
    - **Validate Stock Algorithm**: 주식 알고리즘을 검증합니다.

## 파일 설명

### stock_investing_gui.py

목적: 다른 스크립트의 기능을 통합하는 주요 GUI 스크립트.

주요 함수:
- `crawl_and_save_stock_data()`: 주식 데이터를 크롤링하여 CSV 파일로 저장합니다.
- `create_stock_data_directories()`: 주식 데이터에 필요한 디렉토리를 생성합니다.
- `open_crawling_window()`: 주식 지표를 생성하는 창을 엽니다.
- `open_visualization_window()`: 시각화 버전을 선택하는 창을 엽니다.
- `open_visualization_version1_window()`: 첫 번째 버전의 시각화 창을 엽니다.
- `open_visualization_version2_window()`: 두 번째 버전의 시각화 창을 엽니다.
- `validate_stock_algorithm_window()`: 주식 알고리즘을 검증하는 창을 엽니다.
- `main()`: GUI를 시작하는 메인 함수입니다.

### Listed_Stock_Data_Crawling.py

목적: 상장 주식 데이터를 크롤링하여 주식 코드 및 상장일 등의 정보를 가져옵니다.

주요 함수:
- `stock_code_crawling()`: 주식 코드를 크롤링하여 데이터프레임으로 반환합니다.
- `stock_name_checker()`: 주식 이름이 존재하는지 확인합니다.
- `find_stock_code()`: 주식 이름을 이용해 주식 코드를 찾습니다.

### Save_All_Stock_Data.py

목적: 주식 데이터를 크롤링하여 CSV 파일로 저장합니다.

주요 함수:
- `save_all_stock_data_to_csv()`: 주식 데이터를 크롤링하여 CSV 파일로 저장합니다.

### investment_simulator.py

목적: 투자 시뮬레이션을 수행하여 주식의 매수/매도 조건을 기반으로 수익률을 계산합니다.

주요 함수:
- `simulate_investment()`: 주식 데이터를 기반으로 매수/매도 조건을 적용하여 투자 시뮬레이션을 수행합니다.

### stock_indicators.py

목적: 다양한 주식 지표를 계산하고 CSV 파일로 저장합니다.

주요 함수:
- `calculate_bollinger_bands()`: 볼린저 밴드를 계산합니다.
- `bollinger_bands_for_all()`: 모든 주식에 대해 볼린저 밴드를 계산하여 저장합니다.
- `day2weekNmonth()`: 일별 데이터를 주별 및 월별 데이터로 변환합니다.
- `all_stock_data_day2weekNmonth()`: 모든 주식의 일별 데이터를 주별 및 월별 데이터로 변환합니다.
- `caculate_moving_average()`: 이동 평균을 계산합니다.
- `create_moving_average()`: 특정 기간에 대한 이동 평균을 생성합니다.
- `create_basic_moving_average()`: 기본 이동 평균을 생성합니다.
- `ma4all()`: 모든 주식에 대해 이동 평균을 계산하여 저장합니다.
- `calculate_macd()`: MACD를 계산합니다.
- `create_macd_data()`: MACD 데이터를 생성합니다.
- `create_all_macd()`: 모든 주식에 대해 MACD를 계산하여 저장합니다.
- `calculate_rsi()`: RSI를 계산합니다.
- `create_rsi_all_csv()`: 모든 주식에 대해 RSI를 계산하여 저장합니다.

### visualization_functions.py

목적: 주식 데이터를 시각화합니다.

주요 함수:
- `find_nearest_date()`: 주어진 날짜와 가장 가까운 이전 날짜를 찾습니다.
- `stock_info_Visualization()`: 선택한 지표와 날짜 범위에 따라 주식 데이터를 시각화합니다.

### visualization_v2.py

목적: 주식 데이터를 시각화합니다.

주요 함수:
- `find_nearest_date()`: 주어진 날짜와 가장 가까운 이전 날짜를 찾습니다.
- `stock_info_Visualization_v2()`: 매수일과 매도일을 기준으로 주식 데이터를 시각화합니다.
