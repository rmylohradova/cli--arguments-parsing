import requests
from count_lib import *


def count_encounters_batch():
    word_to_count = sys.argv[1]
    links_file = sys.argv[2]
    output_format_input = sys.argv[3]
    option_name = re.search('^--output-format=(\w)*$', output_format_input)
    if not option_name:
        raise InvalidArgument('Error. Try syntax: --output-format=print or --output-format=csv')
    with open(links_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            link = line.rstrip("\n")
            r = requests.get(link).text
            encounters_list = count_encounters_in_text(r, word_to_count)
            output_format = output_format_input.split('=')[-1]
            list_output_format(encounters_list, output_format, word_to_count, link)

if __name__ == '__main__':
    count_encounters_batch()
