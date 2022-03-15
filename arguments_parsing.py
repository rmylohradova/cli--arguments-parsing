import argparse
from count_lib import count_encounters_in_text, counting_total
import requests
import csv
import sqlite3
from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument('links_file', type=str, help='This is a file with links to analyse')
parser.add_argument('word', type=str, help='Word to count')
parser.add_argument('--output_format', required=True, type=str, choices=['print', 'csv', 'sqlite'], help='How to store the list: print, csv or sqlite')
parser.add_argument('--filename', type=str, help='Specify the filename like *.csv or *.sqlite')
parser.add_argument('--print_total', action='store_true', help='Print total number of encounters per text')
parser.add_argument('--sqlite_table', action='store_true', help='Show database of words and encounters')

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
                            url TEXT,
                            word TEXT,
                            line_index INTEGER,
                            count INTEGER
                           ); """
    cur.execute(create_table)
    cur.execute('SELECT * FROM encounters WHERE url=? and word=?', (url, word))
    exist = cur.fetchone()
    if exist is None:
        for index, count in enumerate(list):
            cur.execute('INSERT INTO encounters VALUES (?,?,?,?)', (url, word, index, count))
    connection.commit()
    connection.close()


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
                connect = sqlite3.connect(args.filename)
                cursor = connect.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS search_words( 
                                             id INTEGER NOT NULL, 
                                             word TEXT, 
                                             PRIMARY KEY(id))''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS sources(
                                            id INTEGER NOT NULL, 
                                            url TEXT,
                                            PRIMARY KEY(id))''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS counts(
                                            word_id INTEGER, 
                                            source_id INTEGER,
                                            line_index INTEGER, 
                                            counts INTEGER)''')
                cursor.execute('SELECT * FROM sources WHERE url=(?)', (link,))
                exist_link = cursor.fetchone()
                cursor.execute('SELECT * FROM search_words WHERE word=(?)', (args.word,))
                exist_word = cursor.fetchone()
                if exist_link is None and exist_word is None:
                    cursor.execute("INSERT INTO search_words(word) VALUES (?)", (args.word,))
                    cursor.execute("INSERT INTO sources(url) VALUES (?)", (link,))
                    word_id = cursor.execute("SELECT id FROM search_words WHERE word=(?)", (args.word,)).fetchone()[0]
                    link_id = cursor.execute("SELECT id FROM sources WHERE url=(?)", (link,)).fetchone()[0]
                    for index, count in enumerate(occur_list):
                        cursor.execute("INSERT INTO counts VALUES (?,?,?,?)", (word_id, link_id, index, count))
                elif exist_link is None and exist_word:
                    cursor.execute("INSERT INTO sources(url) VALUES (?)", (link,))
                    link_id = cursor.execute("SELECT id FROM sources WHERE url=(?)", (link,)).fetchone()[0]
                    word_id = cursor.execute("SELECT id FROM search_words WHERE word=(?)", (args.word,)).fetchone()[0]
                    for index, count in enumerate(occur_list):
                        cursor.execute("INSERT INTO counts VALUES (?,?,?,?)", (word_id, link_id, index, count))
                elif exist_link and exist_word is None:
                    cursor.execute("INSERT INTO search_words(word) VALUES (?)", (args.word,))
                    link_id = cursor.execute("SELECT id FROM sources WHERE url=(?)", (link,)).fetchone()[0]
                    word_id = cursor.execute("SELECT id FROM search_words WHERE word=(?)", (args.word,)).fetchone()[
                        0]
                    for index, count in enumerate(occur_list):
                        cursor.execute("INSERT INTO counts VALUES (?,?,?,?)", (word_id, link_id, index, count))
                elif exist_link and exist_word:
                    link_id = cursor.execute("SELECT id FROM sources WHERE url=(?)", (link,)).fetchone()[0]
                    word_id = cursor.execute("SELECT id FROM search_words WHERE word=(?)", (args.word,)).fetchone()[
                        0]
                    for index, count in enumerate(occur_list):
                        cursor.execute("INSERT INTO counts VALUES (?,?,?,?)", (word_id, link_id, index, count))
                if args.sqlite_table:
                    table = """select search_words.word, counts.line_index,
                        counts.counts, sources.url from counts inner 
                        join search_words on counts.word_id=search_words.id 
                        inner join sources on counts.source_id=sources.id"""
                    print(tabulate(cursor.execute(table), headers=['Search_word', 'Paragraph', 'Encounters per paragraph', 'Text from']))
                connect.commit()
        connect.close()



if __name__ == '__main__':
    arg_parse_count()
