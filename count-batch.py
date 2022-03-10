import requests
import sys

word_to_count = sys.argv[1]


def count_encounters_in_text(text_object, word):
    lines = text_object.split("\n\r")
    total = 0
    for index, line in enumerate(lines):
        encounters = line.count(word)
        total = total + encounters
        print('{i}th paragraph: {e}'.format(i=index, e=encounters))
    print('In the whole text: {t} encounters'.format(t=total))


links_file = sys.argv[2]


def count_encounters_batch(file, word):
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            link = line.rstrip("\n")
            print("Analysing a new text from", link)
            r = requests.get(link).text
            count_encounters_in_text(r, word)

count_encounters_batch(links_file, word_to_count)
