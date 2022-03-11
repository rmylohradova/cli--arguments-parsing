import requests
import sys
from count_lib import count_encounters_in_text

def executing_count():
    text_link = sys.argv[1]
    word_to_count = sys.argv[2]
    text_to_analyse = requests.get(text_link).text
    count_encounters_in_text(text_to_analyse, word_to_count)

if __name__ == '__main__':
    executing_count()



