"""
Scrapes historical answers from sbsolver.com and adds their answers to dictionary.txt
"""
import requests
from bs4 import BeautifulSoup
from scrape import scrape

FILENAME = 'dictionary.txt'
START = 2288
END = START+10

def append(word: str):
    """
    Appends a string to the end of a text file.
    """
    with open(FILENAME, 'a') as f:
        f.write(word+'\n')


def update_dictionary(words, file=FILENAME):
    with open(file) as f:
        dictionary = set(f.read().splitlines())

    # Only add words that are not already in the dictionary file
    new_words = {word for word in words if word not in dictionary}

    with open(file, 'a') as f:
        for word in new_words:
            f.write(word+'\n')

    print(f'{len(new_words)} new words added to {file}')


def main():
    """
    Scrapes historical answers from sbsolver.com and adds their answers to dictionary.txt
    """
    # Solutions are numbered numerically, i.e. "https://www.sbsolver.com/s/1234"
    URL_BASE = 'https://www.sbsolver.com/s/'
    total_words = set()
    for num in range(START,END):
        url = URL_BASE + str(num)

        try:
            print(f'Loading {url}')
            content = requests.get(url).text
        except:
            print(f"Unable to load {url}. Aborting and saving progress!")
            break

        new_words = scrape(content)
        print(f'{len(new_words)} words found.')

        old_len = len(total_words) # Get old length to count new words
        total_words.update(new_words)
        print(f'{len(total_words)-old_len} new words found.')
        print(f'{len(total_words)} total words.\n')

    # We update the dictionary after grabbing a chunk of words to avoid repetitive file I/O ops.
    update_dictionary(total_words)


if __name__ == "__main__":
    main()