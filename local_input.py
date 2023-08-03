import input_detection

def manual_input():

    man_choose = input('Enter text, URL, pdf or txt file path: ')

    if man_choose:
        input_detection.input_detection(man_choose)


manual_input()