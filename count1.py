import requests
import sys
from count_lib import count_encounters_in_text, counting_total

def executing_count():
    text_link = sys.argv[1]
    word_to_count = sys.argv[2]
    text_to_analyse = requests.get(text_link).text
    encounters_list = count_encounters_in_text(text_to_analyse, word_to_count)
    for i in range(0, len(encounters_list)):
        print('{i}th paragraph: {e}'.format(i=i, e=encounters_list[i]))
    print("The total count for this text", counting_total(encounters_list))


if __name__ == '__main__':
    executing_count()



