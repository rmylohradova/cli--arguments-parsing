import requests
import sys


def count_encounters_in_text(text_object, word):
    lines = text_object.split("\n\r")
    total = 0
    for index, line in enumerate(lines):
        encounters = line.count(word)
        total = total + encounters
        print('{i}th paragraph: {e}'.format(i=index, e=encounters))
    print('In the whole text: {t} encounters'.format(t=total))

def executing_count():
    text_link = sys.argv[1]
    word_to_count = sys.argv[2]
    text_to_analyse = requests.get(text_link).text
    count_encounters_in_text(text_to_analyse, word_to_count)

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