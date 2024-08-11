"""
Scrapes historical answers from sbsolver.com and adds their answers to dictionary.txt
"""

import requests
from bs4 import BeautifulSoup

FILENAME = 'dictionary.txt'

def get_answers(html_file):
    # Answers are found in a tag <td class="bee-hover"> with a link to
    # "https://www.sbsolver.com/h/" + the answer.
    soup = BeautifulSoup(html_file, 'html.parser')
    # Filter tags using  <td> and class="bee-hover"
    bee_hovers = soup.find_all('td', class_="bee-hover")
    # Use the sbsolver URL to mark the start of the answer word.
    marker = 'https://www.sbsolver.com/h/'
    words = set()
    for tag in bee_hovers:
        line = str(tag)
        # The word begins after the URL
        idx_begin = line.index(marker)+len(marker)
        line = line[idx_begin:]
        # The word ends with a "
        idx_end = line.index('"')
        # Convert to upper case to match the dictionary.txt format
        line = line[:idx_end].upper()
        words.add(line)
    return words


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
    urls = ['https://www.sbsolver.com/s/'+str(num) for num in range(1200,2287)] #2287

    total_words = set()
    for url in urls:
        print(f'Loading {url}')
        content = requests.get(url).text
        new_words = get_answers(content)
        print(f'{len(new_words)} words found.')
        total_words.update(new_words)
        print(f'{len(total_words)} total words.\n')

    # We update the dictionary after grabbing a chunk of words to avoid repetitive file I/O ops.
    update_dictionary(total_words)


if __name__ == "__main__":
    main()