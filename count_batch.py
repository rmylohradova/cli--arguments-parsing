import requests
import sys
from count_lib import count_encounters_in_text


def count_encounters_batch():
    word_to_count = sys.argv[1]
    links_file = sys.argv[2]
    with open(links_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            link = line.rstrip("\n")
            print("Analysing a new text from", link)
            r = requests.get(link).text
            count_encounters_in_text(r, word_to_count)

if __name__ == '__main__':
    count_encounters_batch()
