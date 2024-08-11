"""
Scrapes historical answers from sbsolver.com and adds their answers to dictionary.txt
"""

import requests
from bs4 import BeautifulSoup

FILENAME = 'dictionary.txt'

def get_answers(html_file):
    # Answers are found inside tags <td class="bee-hover"><a>
    soup = BeautifulSoup(html_file, 'html.parser')
    answers = soup.find_all('td', class_='bee-hover')
    return {answer.a.text for answer in answers}


def append(word: str):
    """
    Appends a string to the end of a text file.
    """
    with open(FILENAME, 'a') as f:
        f.write(word+'\n')


def update_dictionary(words):
    with open(FILENAME) as f:
        dictionary = set(f.read().splitlines())

    # Only add words that are not already in the dictionary file
    new_words = {word for word in words if word not in dictionary}

    with open(FILENAME, 'a') as f:
        for word in new_words:
            f.write(word+'\n')

    print(f'{len(new_words)} new words added to {FILENAME}')


def main():
    """
    Scrapes historical answers from sbsolver.com and adds their answers to dictionary.txt
    """
    # Solutions are numbered numerically, i.e. "https://www.sbsolver.com/s/1234"
    URL_BASE = 'https://www.sbsolver.com/s/'
    total_words = set()
    for num in range(2286,2288):
        url = URL_BASE + str(num)

        try:
            print(f'Loading {url}')
            content = requests.get(url).text
        except:
            print(f"Unable to load {url}. Aborting and saving progress!")
            break

        new_words = get_answers(content)
        print(f'{len(new_words)} words found.')

        old_len = len(total_words) # Get old length to count new words
        total_words.update(new_words)
        print(f'{len(total_words)-old_len} new words found.')
        print(f'{len(total_words)} total words.\n')

    # We update the dictionary after grabbing a chunk of words to avoid repetitive file I/O ops.
    update_dictionary(total_words)


if __name__ == "__main__":
    main()