import argparse
from count_lib import count_encounters_in_text, counting_total
import requests
import csv
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('links_file', type=str, help='This is a file with links to analyse')
parser.add_argument('word', type=str, help='Word to count')
parser.add_argument('--output_format', required=True, type=str, choices=['print', 'csv', 'sqlite'], help='How to store the list: print, csv or sqlite')
parser.add_argument('--filename', type=str, help='Specify the filename like *.csv or *.sqlite')
parser.add_argument('--print_total', action='store_true')


def write_to_csv(file, link, list, word):
    with open(file, 'a') as csvfile:
        fieldnames = ['url', 'word', 'line_index', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0, len(list)):
            writer.writerow({'url': link, 'word': word, 'line_index': i, 'count': list[i]})
        return file


def write_to_sqlite(file, url, list, word):
    connection = sqlite3.connect(file)
    cur = connection.cursor()
    create_table = """CREATE TABLE IF NOT EXISTS encounters (
                            url VARCHAR(255) NOT NULL,
                            word CHAR(30),
                            line_index INT,
                            count INT
                           ); """
    cur.execute(create_table)
    cur.execute('SELECT * FROM encounters WHERE url=? and word=?', (url, word))
    exist = cur.fetchone()
    print(exist)
    if exist is None:
        for index, count in enumerate(list):
            cur.execute('INSERT INTO encounters VALUES (?,?,?,?)', (url, word, index, count))
    else:
        pass
    connection.commit()
    connection.close()
    return connection

def arg_parse_count():
    args = parser.parse_args()
    with open(args.links_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            link = line.rstrip("\n")
            text_to_analyse = requests.get(link).text
            occur_list = count_encounters_in_text(text_to_analyse, args.word)
            if args.output_format == 'print':
                print("Analysing a new text from", link)
                for i in range(0, len(occur_list)):
                    print('{i}th paragraph: {e}'.format(i=i, e=occur_list[i]))
                if args.print_total:
                    print("The total count for this text", counting_total(occur_list))
            elif args.output_format == 'csv':
                write_to_csv(args.filename, link, occur_list, args.word)
            elif args.output_format == 'sqlite':
                write_to_sqlite(args.filename, link, occur_list, args.word)


if __name__ == '__main__':
    arg_parse_count()
