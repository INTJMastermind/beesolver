FILENAME = 'dictionary.txt'

def append(word: str):
    """
    Appends a string to the end of a text file.
    """
    with open(FILENAME, 'a') as f:
        f.write(word+'\n')
        

def readfile():
    with open(FILENAME) as f:
        return set(f.read().splitlines())
    

def main():
    dictionary = readfile()
    added_words = set()

    while True:
        word = input(f"Append word to {FILENAME} (CTRL+C to Abort): ").upper()

        if word in dictionary:
            print(f'{word} is already in {FILENAME}.\n')
        elif word in added_words:
            print(f'{word} has already been added.')
        else:
            append(word)
            added_words.add(word)
            print(f'{word} successfully appended to {FILENAME}.\n')

if __name__ == '__main__':
    main()