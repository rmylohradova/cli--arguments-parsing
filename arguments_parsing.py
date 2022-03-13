import argparse
from count_lib import count_encounters_in_text, counting_total
import requests
import csv

parser = argparse.ArgumentParser()
parser.add_argument('text_link', type=str, help='This is a link to the text you want to analyse')
parser.add_argument('word', type=str, help='Word to count')
parser.add_argument('--output_format', required=True, type=str, choices=['print', 'csv'], help='How to store the list: print or csv')
parser.add_argument('--filename', type=str, help='Specify the filename like *.csv')
parser.add_argument('--print_total', action='store_true')



def arg_parse_count():
    args = parser.parse_args()
    text_to_analyse = requests.get(args.text_link).text
    occur_list = count_encounters_in_text(text_to_analyse, args.word)
    if args.output_format == 'print':
        print("Analysing a new text from", args.text_link)
        for i in range(0, len(occur_list)):
            print('{i}th paragraph: {e}'.format(i=i, e=occur_list[i]))
        if args.print_total:
            print("The total count for this text", counting_total(occur_list))
    elif args.output_format == 'csv':
        with open(args.filename, 'a') as csvfile:
            fieldnames = ['url', 'word', 'line_index', 'count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, len(occur_list)):
                writer.writerow({'url': args.text_link, 'word': args.word, 'line_index': i, 'count': occur_list[i]})
    else:
        print("The output method is not specified, please choose between 'print' and 'csv'")


if __name__ == '__main__':
    arg_parse_count()
