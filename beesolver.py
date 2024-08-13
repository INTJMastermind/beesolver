def load(file_name):
    '''
    Input: "file_name": a string that points to the dictionary of allowed words.
    Output: A set of strings corresponding to the contents of that dictionary.
    '''
    try:
        with open(file_name) as file:
            word_list = file.read().splitlines()
        return set(word_list)
    except:
        return set()    


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

    word = word.upper()

    # Check for mandatory letter
    if letters[0] not in word:
        return False

    # Check for a letter not in the word
    for letter in word:
        if letter not in letters:
            return False

    return True


def solve(letters, words):
    '''
    Input: A string of letters and a set of possible words.
    Output: Returns a list valid words.
    '''
    return [word for word in words if check_word(word, letters) == True]


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


def main():
    FILE_NAME = 'dictionary.txt' # Name of dictionary file
    words = load(FILE_NAME)

    letters = input("Enter the game's letters without spaces. The first letter must be the center / mandatory letter: ")
    letters = list(letters.upper())

    answers = solve(letters, words)
    scores = [score_word(word, letters) for word in answers]

    print(f'\n{len(answers)} possible words found.')
    print(f'Total score: {sum(scores)}\n')

    for word, score in zip(answers, scores):
        print(f'{word} - {score}')


if __name__ == '__main__':
    main()