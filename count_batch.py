import requests
from count_lib import *


def count_encounters_batch():
    word_to_count = sys.argv[1]
    links_file = sys.argv[2]
    with open(links_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            link = line.rstrip("\n")
            r = requests.get(link).text
            encounters_list = count_encounters_in_text(r, word_to_count)
            list_output_format(encounters_list, word_to_count, link)

if __name__ == '__main__':
    count_encounters_batch()
