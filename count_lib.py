import sys
import re
import csv


class InvalidArgument(Exception):
    pass


class InvalidFileName(Exception):
    pass


def count_encounters_in_text(text_object, word):
    lines = text_object.split("\n\r")
    encounters_list = []
    for line in lines:
        encounters_in_line = line.count(word)
        encounters_list.append(encounters_in_line)
    return encounters_list


def counting_total(list):
    return sum(list)


def list_output_format(input_list, word, link):
    output_format_input = sys.argv[3]
    option_name = re.search('^--output-format=(\w)*$', output_format_input)
    if not option_name:
        raise InvalidArgument('Error. Try syntax: --output-output_format=print or --output-output_format=csv')
    output_format = output_format_input.split('=')[-1]
    if output_format == 'print':
        for i in range(0, len(input_list)):
            print('{i}th paragraph: {e}'.format(i=i, e=input_list[i]))
        print("The total count for this text", counting_total(input_list))
    elif output_format == 'csv':
        filename_input = sys.argv[4]
        match = re.search('^--filename=(\w)*(.)[c][s][v]$', filename_input)
        if not match:
            raise InvalidFileName("Error. Try syntax: --filename=*.csv")
        filename = filename_input.split('=')[-1]
        with open(filename, 'a') as csvfile:
            fieldnames = ['url', 'word', 'line_index', 'count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, len(input_list)):
                writer.writerow({'url': link, 'word': word, 'line_index': i, 'count': input_list[i]})
            return filename
    else:
        print("The output method is not specified, please choose between 'print' and 'csv'")
