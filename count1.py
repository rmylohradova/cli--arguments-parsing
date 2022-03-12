import requests
import sys
from count_lib import count_encounters_in_text, counting_total
import csv
import re

def executing_count():
    text_link = sys.argv[1]
    word_to_count = sys.argv[2]
    output_format = sys.argv[3]
    class InvalidArgument(Exception):
        pass
    if output_format != '--output-format=print' and output_format != '--output-format=csv':
        raise InvalidArgument('Error. Try syntax: --output-format=print or --output-format=csv')
    text_to_analyse = requests.get(text_link).text
    encounters_list = count_encounters_in_text(text_to_analyse, word_to_count)
    if 'print' in output_format:
        for i in range(0, len(encounters_list)):
            print('{i}th paragraph: {e}'.format(i=i, e=encounters_list[i]))
        print("The total count for this text", counting_total(encounters_list))
    elif 'csv' in output_format:
        filename_input = sys.argv[4]
        class InvalidFileName(Exception):
            pass
        match = re.search('^--filename=(\w)*(.)[c][s][v]$', filename_input)
        if not match:
            raise InvalidFileName("Error. Try syntax: --filename=*.csv")
        filename = filename_input.split('=')[-1]
        with open(filename, 'w') as csvfile:
            fieldnames = ['url', 'word', 'line_index', 'count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, len(encounters_list)):
                writer.writerow({'url': text_link, 'word': word_to_count, 'line_index': i, 'count': encounters_list[i]})
    else:
        print("The output method is not specified, please choose between 'print' and 'csv'")



if __name__ == '__main__':
    executing_count()


