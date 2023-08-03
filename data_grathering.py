import text_processing
import urllib.request
import PyPDF2
from Crypto.Cipher import AES

def pdf_input(path):
    with open(path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        text_processing.normal_start(text)



def txt_input(path):
    with open(path, 'r') as file:
        text = file.read()
    text_processing.normal_start(text)


def str_input(text_str):
    text_processing.normal_start(text_str)

#web scrabling
def url_input(link):
    text = urllib.request.urlopen(link)
    article = text.read()
    text_processing.url_start(article)