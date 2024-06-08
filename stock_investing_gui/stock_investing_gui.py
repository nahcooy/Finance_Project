import PySimpleGUI as sg
import pandas as pd
import os
from Listed_Stock_Data_Crawling import stock_code_crawling
from Save_All_Stock_Data import save_all_stock_data_to_csv
from stock_indicators import (
    bollinger_bands_for_all,
    all_stock_data_day2weekNmonth,
    ma4all,
    create_all_macd,
    create_rsi_all_csv
)
from visualization_functions import stock_info_Visualization


# 주식 데이터 크롤링 함수 호출 및 저장
def crawl_and_save_stock_data(base_dir):
    try:
        print("Starting stock data crawling...")
        stock_info = stock_code_crawling()
        gui_dir = os.path.join(base_dir, 'stock_investing_gui')
        stock_info_path = os.path.join(gui_dir, 'stock_codes.csv')
        stock_info.to_csv(stock_info_path, index=False, encoding='cp949')
        save_all_stock_data_to_csv(stock_info, base_dir)
        sg.popup('Stock data has been successfully crawled and saved!')
        print("Stock data crawling completed.")
    except Exception as e:
        sg.popup(f'An error occurred: {e}')
        print(f"Error occurred during stock data crawling: {e}")


def create_stock_data_directories(base_dir):
    print(f"Creating stock data directories in {base_dir}...")
    gui_dir = os.path.join(base_dir, 'stock_investing_gui')
    stock_data_dir = os.path.join(gui_dir, 'stock_data')
    subdirs = ['day', 'ma', 'macd', 'month', 'RSI', 'special', 'week', 'BB']
    vis_dir = os.path.join(gui_dir, 'vis')
    os.makedirs(stock_data_dir, exist_ok=True)
    os.makedirs(vis_dir, exist_ok=True)
    for subdir in subdirs:
        os.makedirs(os.path.join(stock_data_dir, subdir), exist_ok=True)
    print(f"Directories created: {subdirs}")
    return gui_dir


def open_crawling_window(base_dir):
    print("Opening crawling window...")
    layout = [
        [sg.Text('Choose an option to create:', size=(40, 1), font=("Helvetica", 25), justification='center')],
        [sg.Column([[sg.Button('Create Daily Prices', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('Create Bollinger Bands', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('Create WeeklyNMonthly Prices', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('Create Moving Averages (MA)', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('Create Moving Averages (MA)', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('Create MACD', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('Create RSI', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('Create All', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('Back', size=(30, 2), font=("Helvetica", 15))]], justification='center')]
    ]

    new_window = sg.Window('Create Stock Indicators', layout, size=(700, 900), finalize=True)
    new_window.TKroot.resizable(False, False)
    gui_dir = os.path.join(base_dir, 'stock_investing_gui')
    stock_info_path = os.path.join(gui_dir, 'stock_codes.csv')

    while True:
        event, values = new_window.read()
        print(f"Event: {event}, Values: {values}")
        if event == sg.WINDOW_CLOSED or event == 'Back':
            break
        if event == 'Create Daily Prices':
            print("Creating Daily Prices...")
            crawl_and_save_stock_data(base_dir)
        elif not os.path.exists(stock_info_path):
            sg.popup('Please create daily prices first by clicking "Create Daily Prices".')
            print("Daily prices not created yet.")
        elif event == 'Create Bollinger Bands':
            print("Creating Bollinger Bands...")
            bollinger_bands_for_all(base_dir)
            sg.popup('Bollinger Bands creation completed.')
        elif event == 'Create Weekly Prices':
            print("Creating WeeklyNMonthly Prices...")
            all_stock_data_day2weekNmonth(base_dir)
            sg.popup('Weekly Prices creation completed.')
        elif event == 'Create Moving Averages (MA)':
            print("Creating Moving Averages (MA)...")
            ma4all(base_dir)
            sg.popup('Moving Averages (MA) creation completed.')
        elif event == 'Create MACD':
            print("Creating MACD...")
            create_all_macd(base_dir)
            sg.popup('MACD creation completed.')
        elif event == 'Create RSI':
            print("Creating RSI...")
            create_rsi_all_csv(base_dir)
            sg.popup('RSI creation completed.')
        elif event == 'Create All':
            print("Creating all indicators...")
            print("Creating Bollinger Bands...")
            bollinger_bands_for_all(base_dir)
            print("Creating WeeklyNMonthly Prices...")
            all_stock_data_day2weekNmonth(base_dir)
            print("Creating Moving Averages (MA)...")
            ma4all(base_dir)
            print("Creating MACD...")
            create_all_macd(base_dir)
            print("Creating RSI...")
            create_rsi_all_csv(base_dir)
            sg.popup('All indicators creation completed.')

    new_window.close()
    print("Crawling window closed.")

def open_visualization_window(base_dir):
    print("Opening visualization window...")
    layout = [
        [sg.Text('Choose Visualization Version:', size=(40, 1), font=("Helvetica", 25), justification='center')],
        [sg.Column([[sg.Button('시각화 ver1', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('시각화 ver2', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('Back', size=(30, 2), font=("Helvetica", 20))]], justification='center')]
    ]

    new_window = sg.Window('Stock Data Visualization', layout, size=(500, 350), finalize=True, location=(None, None))
    new_window.TKroot.resizable(False, False)

    while True:
        event, values = new_window.read()
        print(f"Event: {event}, Values: {values}")
        if event == sg.WINDOW_CLOSED or event == 'Back':
            break
        if event == '시각화 ver1':
            open_visualization_version1_window(base_dir)
        if event == '시각화 ver2':
            sg.popup('Visualization ver2 not yet implemented.')

    new_window.close()
    print("Visualization window closed.")

def open_visualization_version1_window(base_dir):
    print("Opening visualization version 1 window...")
    subdirs = ['day', 'ma', 'macd', 'RSI', 'special', 'BB']
    layout = [
        [sg.Text('Select Data to Visualize:', size=(40, 1), font=("Helvetica", 25), justification='center')],
        [sg.Column([[sg.Checkbox(subdir, key=subdir) for subdir in subdirs]], justification='center')],
        [sg.Text('Select Start Date (YYYY-MM-DD):', font=("Helvetica", 15))],
        [sg.Input(key='start_date', size=(20, 1)),
         sg.CalendarButton('Select Date', target='start_date', format='%Y-%m-%d')],
        [sg.Text('Select End Date (YYYY-MM-DD):', font=("Helvetica", 15))],
        [sg.Input(key='end_date', size=(20, 1)),
         sg.CalendarButton('Select Date', target='end_date', format='%Y-%m-%d')],
        [sg.Column([[sg.Button('Visualize', size=(30, 2), font=("Helvetica", 20))]], justification='center')],
        [sg.Column([[sg.Button('Back', size=(30, 2), font=("Helvetica", 20))]], justification='center')]
    ]

    window_width, window_height = 700, 500
    screen_width, screen_height = sg.Window.get_screen_size()
    location = (screen_width // 2 - window_width // 2, screen_height // 2 - window_height // 2)

    new_window = sg.Window('Visualization ver1', layout, size=(window_width, window_height), location=location,
                           finalize=True)
    new_window.TKroot.resizable(False, False)

    while True:
        event, values = new_window.read()
        print(f"Event: {event}, Values: {values}")
        if event == sg.WINDOW_CLOSED or event == 'Back':
            break
        if event == 'Visualize':
            selected_subdirs = [subdir for subdir in subdirs if values[subdir]]
            start_date = values['start_date']
            end_date = values['end_date']

            if not selected_subdirs:
                sg.popup('No data selected for visualization.')
                print("No data selected for visualization.")
            elif not start_date or not end_date:
                sg.popup('Please select both start and end dates.')
                print("Start date or end date not selected.")
            else:
                stock_info_path = os.path.join(base_dir, 'stock_codes.csv')
                stock_info = pd.read_csv(stock_info_path)
                stock_name = 'AAPL'  # Example stock name
                listing_date = stock_info.loc[stock_info['company'] == stock_name, 'listing_date'].values[0]

                if pd.to_datetime(start_date) < pd.to_datetime(listing_date):
                    sg.popup(
                        f'Start date {start_date} is before the listing date {listing_date} of {stock_name}. Please select a valid start date.')
                    print(f"Invalid start date: {start_date} is before listing date: {listing_date}")
                else:
                    print(f"Visualizing data for {stock_name} from {start_date} to {end_date}")
                    visualize_stock_data(base_dir, selected_subdirs, stock_name, start_date, end_date)

    new_window.close()
    print("Visualization version 1 window closed.")

def visualize_stock_data(base_dir, selected_subdirs, stock_name, start_date, end_date):
    print(f"Visualizing stock data for {stock_name} from {start_date} to {end_date}")
    layout = [
        [sg.Canvas(key='canvas')],
        [sg.Button('Save', size=(10, 1)), sg.Button('Close', size=(10, 1))]
    ]

    window = sg.Window('Stock Data Visualization', layout, finalize=True, location=(None, None))
    window.TKroot.resizable(False, False)

    fig = stock_info_Visualization(stock_name, start_date, end_date, selected_subdirs)

    while True:
        event, values = window.read()
        print(f"Event: {event}, Values: {values}")
        if event == sg.WINDOW_CLOSED or event == 'Close':
            break
        if event == 'Save':
            print("Saving visualization...")
            save_visualization(fig, stock_name, start_date, end_date, base_dir)

    window.close()
    print("Stock data visualization window closed.")


def save_visualization(fig, stock_name, start_date, end_date, base_dir):
    save_directory = os.path.join(base_dir, 'vis')
    os.makedirs(save_directory, exist_ok=True)
    save_path = os.path.join(save_directory, f'{stock_name}_{start_date}_{end_date}_visualization.png')
    fig.savefig(save_path)
    sg.popup(f'Visualization saved to {save_path}')
    print(f"Visualization saved to {save_path}")


# 메인 함수
def main():
    sg.theme('LightBlue2')

    layout = [
        [sg.Text('Choose an option', size=(40, 1), font=("Helvetica", 25), justification='center')],
        [sg.Button('Set Base Dir', size=(30, 2), font=("Helvetica", 20))],
        [sg.Button('Crawl Stock Data', size=(30, 2), font=("Helvetica", 20))],
        [sg.Button('Visualize Stock Data', size=(30, 2), font=("Helvetica", 20))],
        [sg.Button('Validate Stock Algorithm', size=(30, 2), font=("Helvetica", 20))],
        [sg.Button('Exit', size=(30, 2), font=("Helvetica", 20))]
    ]

    layout = [[sg.Column(layout, element_justification='center', vertical_alignment='center')]]

    window = sg.Window('Stock Investment Tool', layout, size=(700, 550), finalize=True)
    window.TKroot.resizable(False, False)

    base_dir = None

    while True:
        event, values = window.read()
        print(f"Event: {event}, Values: {values}")
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        if event == 'Set Base Dir':
            base_dir = sg.popup_get_folder('Select Base Directory')
            if base_dir:
                gui_dir = create_stock_data_directories(base_dir)
                sg.popup(f'Base directory set to: {gui_dir}')
                print(f"Base directory set to: {gui_dir}")

        if event == 'Crawl Stock Data':
            if not base_dir:
                sg.popup('Please set the base directory first.')
                print("Base directory not set.")
            else:
                open_crawling_window(base_dir)

        if event == 'Visualize Stock Data':
            if not base_dir:
                sg.popup('Please set the base directory first.')
                print("Base directory not set.")
            else:
                open_visualization_window(base_dir)

        if event == 'Validate Stock Algorithm':
            sg.popup('Stock algorithm validation feature is not yet implemented.')
            print("Stock algorithm validation feature not yet implemented.")

    window.close()
    print("Main window closed.")


if __name__ == '__main__':
    main()
