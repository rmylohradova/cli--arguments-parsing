import requests
from count_lib import *


def executing_count():
    text_link = sys.argv[1]
    word_to_count = sys.argv[2]
    output_format_input = sys.argv[3]
    option_name = re.search('^--output-format=(\w)*$', output_format_input)
    if not option_name:
        raise InvalidArgument('Error. Try syntax: --output-format=print or --output-format=csv')
    text_to_analyse = requests.get(text_link).text
    encounters_list = count_encounters_in_text(text_to_analyse, word_to_count)
    output_format = output_format_input.split('=')[-1]
    list_output_format(encounters_list, output_format, word_to_count, text_link)




if __name__ == '__main__':
    executing_count()


