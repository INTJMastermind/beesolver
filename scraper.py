"""
Scrapes historical answers from sbsolver.com and adds their answers to dictionary.txt
"""
import requests
from bs4 import BeautifulSoup
from scrape import scrape
import beesolver

FILENAME = 'dictionary.txt'
START = 1939
END = 2289


def update_dictionary(words, file=FILENAME):
    with open(file, 'w') as f:
        for word in words:
            f.write(word+'\n')

    print(f'{len(words)} words written to {file}.')


def load_and_prune(file):
    # Load the dictionary and remove any words <4 characters.
    print(f'Loading {file}')
    with open(file) as f:
        dictionary = set(f.read().splitlines())
    
    len_orig = len(dictionary)
    print(f'{len_orig} words loaded')

    # Remove words <4 characters
    dictionary = {word.upper() for word in dictionary if len(word) >= 4}
    print(f'{len_orig - len(dictionary)} words <4 letters pruned.')
    print(f'New length: {len(dictionary)} words.')
    return dictionary

def main():
    """
    Scrapes historical answers from sbsolver.com and adds their answers to dictionary.txt
    """
    # Load a set of dictionary words with words <4 characters pruned out.
    dictionary = load_and_prune(FILENAME)

    # Solutions are numbered numerically, i.e. "https://www.sbsolver.com/s/1234"
    URL_BASE = 'https://www.sbsolver.com/s/'
    for num in range(START,END):
        url = URL_BASE + str(num)
        try:
            print(f'\nLoading {url}')
            content = requests.get(url).text
        except:
            print(f"Unable to load {url}. Aborting and saving progress!")
            break

        # Scrape the puzzle date, letters, and official answers
        date, letters, answers = scrape(content)
        answers = set(answers)
        print(f'Puzzle for {date}: {letters}')
        print(f'{len(answers)} official answers')

        # Generate our own solution set from beesolver
        solutions = set(beesolver.solve(letters, dictionary))
        print(f'{len(solutions)} solutions generated by beesolver')

        # Solutions not in the official answer list will be removed from the dictionary.
        not_solutions = {word for word in solutions if word not in answers}
        for word in not_solutions:
            dictionary.remove(word)
        print(f'{len(not_solutions)} words removed from dictionary.')

        # Answers not in the solution set will be added to the dictionary.
        missing_answers = {word for word in answers if word not in solutions}
        dictionary.update(missing_answers)
        print(f'{len(missing_answers)} words added to dictionary.')

    # We update the dictionary after grabbing a chunk of words to avoid repetitive file I/O ops.
    update_dictionary(dictionary)


if __name__ == "__main__":
    main()