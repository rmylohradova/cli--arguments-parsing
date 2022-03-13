import requests
from count_lib import *


def executing_count():
    text_link = sys.argv[1]
    word_to_count = sys.argv[2]
    text_to_analyse = requests.get(text_link).text
    encounters_list = count_encounters_in_text(text_to_analyse, word_to_count)
    list_output_format(encounters_list, word_to_count, text_link)




if __name__ == '__main__':
    executing_count()


