import data_grathering
import os

class input_detection():
    def __init__(self, data_type):
        
        #URL
        if data_type.startswith('http://') or data_type.startswith('https://'):
            print("URL detected. Calling inputs.url_input.. ")
            data_grathering.url_input(data_type)

        #PDF ot TXT
        elif os.path.isfile(data_type):
            if data_type.endswith('.pdf'):
                print("pdf detected")
                data_grathering.pdf_input(data_type)

            elif data_type.endswith('.txt'):
                print("txt detected")
                data_grathering.txt_input(data_type)

            else:
                print("invalid file extension")

        #str input
        elif isinstance(data_type, str):
            print("data_type str detected, starting the text processing...")
            data_grathering.str_input(data_type)

        else:
            print("incorrect input")