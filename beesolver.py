FILE_NAME = 'dictionary.txt' # Name of dictionary file

def load_words(file_name):
    '''
    Input: "file_name": a string that points to the dictionary of allowed words.
    Output: A set of strings corresponding to the contents of that dictionary.
    '''

    with open(file_name) as file:
        word_list = file.read().splitlines()
    
    return set(word_list)


def check_word(word, letters):
    '''
    Input: word, a string
    Returns whether word is valid per Spelling Bee rules:
    - Must have at least one copy of the first letter.
    - Must NOT have any letters outside the list.
    '''
    # Spelling bee answers must be 4 letters or greater.
    if len(word) < 4:
        return False

    word = word.lower()

    # Check for mandatory letter
    if letters[0] not in word:
        return False

    # Check for a letter not in the word
    for letter in word:
        if letter not in letters:
            return False

    return True


def score_word(word, letters):
    '''
    Scores a valid word by the following rules:
    - Length 4 words get 1 point
    - Longer words are scored by the number of letters.
    - Pangram gets 7 bonus points.
    '''
    if len(word) == 4:
        return 1
   
    score = len(word)
    if all([letter in list(word.lower()) for letter in letters]):
        score += 7
    return score


def beesolver(letters, word_list):
    '''
    Input: None
    Output: Returns a list valid words.
    '''
    return {word: score_word(word, letters) for word in word_list if check_word(word, letters) == True}


def main():
    letters = input('Enter the letters seperated by spaces, the first letter is the mandatory letter: ')
    letters = letters.lower().split(' ')
    words = load_words(FILE_NAME)

    answers = beesolver(letters, words)

    print(f'\n{len(answers)} possible words found.')
    print(f'Total score: {sum(answers.values())}\n')

    for word, score in sorted(answers.items()):
        print(f'{word} - {score}')


if __name__ == '__main__':
    main()