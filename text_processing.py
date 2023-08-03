import re
import nltk
from bs4 import BeautifulSoup
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from heapq import nlargest

#add everything in classes

#parsing / cleaning the url HTML content
def url_start(raw_data):
    article_parsed = BeautifulSoup(raw_data, 'html.parser')
    paragraphs = article_parsed.find_all('p')
    heading = article_parsed.find_all("h1")
    sub_headings = headings = article_parsed.find_all(["h2", "h3", "h4"])
    description = article_parsed.find_all("div", class_="article-description")
    article_summary = article_parsed.find_all("div", class_="article__summary summary ")
    descriptions = description + article_summary
    contents = paragraphs + heading * 8 + descriptions * 2
    article_content = ""

    for p in contents:
        text = p.text.strip()  # Remove leading/trailing whitespaces

        if text and not text.endswith("."):
            text += ". "
        if text and not text.endswith(". "):
            text += " "

        article_content += text

    article_content = article_content
    normal_start(article_content)


def normal_start(raw_data):
    print("Starting the text processing...\n")

    #stop words download
    nltk.download("stopwords")

    #tokenization
    tokens = nltk.word_tokenize(raw_data)


    #make table
    freq_table = make_clean_frequency_table(tokens)
    
    #calculate occurancy ratios
    occ_ratio = calc_occ_ratio(freq_table)

    #title
    pattern = r'The Title:'

    #sentence tokenization
    #clean_data = re.sub(r'\.\s*', '. ', raw_data)
    sentences = nltk.sent_tokenize(raw_data)
    

    #calculate sentence weight
    sentence_weight = calc_sentence_weight(sentences, freq_table)
    

    #summary
    print("printing the summary: ")
    select_length = int(len(sentence_weight) * 1)
    summary = nlargest(select_length, sentence_weight, key=sentence_weight.get)
    sorted_summary = sorted(summary, key=lambda x: sentence_weight[x], reverse=True)

    priority_and_clean = [(i + 1, sentence.replace('\n', '')) for i, sentence in enumerate(sorted_summary[:20])]

    
    html_summary = ""
    for priority, sentence in priority_and_clean:
        html_summary += str(priority) + ": " + sentence + "<br><br>"
        print(f"{priority}: {sentence}")
    print(html_summary)
    ready = input("Press Enter To Exit/Continue")

    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(html_summary)


    

    #calculate word frequency
    #Calculate the weighted frequency for each sentence

    #nltk.download('averaged_perceptron_tagger')
    #tagged = nltk.pos_tag(tokens)

    #print("Here is the tokenized raw data: \n")
    #print(tokens)


def make_clean_frequency_table(tokens):
    stop_words = stopwords.words('english')
    stop_words += ["ja", "ovat", "niin", "kuin", "siitä", "asti", "myös", "siksi", "jotta", "on", "ei", "\n"]
    punctuations = punctuation + "\n"

    word_frequencies = {}
    for word in tokens:
        if word.lower() not in stop_words:
            if word.lower() not in punctuations:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
    
    return word_frequencies

def calc_occ_ratio(freq_table):
    max_frequency = max(freq_table.values())

    for word in freq_table.keys():
        freq_table[word] = freq_table[word]/max_frequency
    return freq_table

### Try to understand everything in this part ###
def calc_sentence_weight(sentences, freq_table):
    sentence_weight = dict()
    for sentence in sentences:
        #adjusting sentence lenght relevancy
        sentence_wordcount = (len(word_tokenize(sentence)))
        multiply = 1
        multiply_changer = 0.99 

        for word in range(sentence_wordcount):
            
            if multiply > 0.1: #minumn multiplier
                multiply = multiply * multiply_changer
                #print(multiply, sentence)

        sentence_wordcount_without_stop_words = 0
        for word_weight in freq_table:


            if word_weight in sentence.lower(): 
                sentence_wordcount_without_stop_words += 1 * multiply
                if sentence in sentence_weight:
                    sentence_weight[sentence] += freq_table[word_weight] * multiply
                else:
                    sentence_weight[sentence] = freq_table[word_weight] * multiply

        try:
            sentence_weight[sentence] = sentence_weight[sentence]
            #print("multiplied sentence weight:", sentence_weight[sentence])
        except:
            pass

    return sentence_weight





