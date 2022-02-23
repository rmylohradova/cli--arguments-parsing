import requests

r = requests.get("https://www.gutenberg.org/cache/epub/67477/pg67477.txt").text

def count_encounters_in_text(text_object, word):
    lines = text_object.split("\n\r")
    total = 0
    for index, line in enumerate(lines):
        encounters = line.count(word)
        total = total + encounters
        print('{i}th paragraph: {e}'.format(i=index, e=encounters))
    print('In the whole text: {t} encounters'.format(t=total))

count_encounters_in_text(r, 'of')



