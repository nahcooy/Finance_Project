import PySimpleGUI as sg

def main():
    # GUI 레이아웃 설정
    layout = [
        [sg.Text('텍스트를 입력하세요:'), sg.InputText(key='input_text')],
        [sg.Button('확인'), sg.Button('종료')]
    ]

    # 창 생성
    window = sg.Window('PySimpleGUI 테스트', layout)

    # 이벤트 루프
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '종료'):
            break

        if event == '확인':
            input_text = values['input_text']
            sg.popup(f'입력된 텍스트: {input_text}')

    window.close()

if __name__ == "__main__":
    main()
