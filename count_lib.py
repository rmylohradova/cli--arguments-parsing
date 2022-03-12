import requests


def count_encounters_in_text(text_object, word):
    lines = text_object.split("\n\r")
    encounters_list = []
    for line in lines:
        encounters_in_line = line.count(word)
        encounters_list.append(encounters_in_line)
    return encounters_list

def counting_total(list):
    return sum(list)
