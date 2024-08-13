import requests
import os
import re
from bs4 import BeautifulSoup

def download(url: str, file_name: str):
    """
    Downloads a website at url and saves it as file_name.
    """
    try:
        r = requests.get(url).text
    except:
        print(f'Unable to load {url}')
        return

    with open(file_name, 'w') as file:
        file.write(r)


def scrape(site):
    """
    Scraper for sbsolver.com. Input is a requests.get(url).text
    """
    soup = BeautifulSoup(site, 'html.parser')

    # Scrape the date
    date = soup.find('span', class_ = re.compile('^bee-date'))
    date = date.a.text

    # Scrape the letters.
    # All the letters are found in a <div class='thinner-space-after>
    # Letters are images, listed in order with the center letter first
    images = soup.find('div', class_='thinner-space-after').find_all('img')
    # Extracting each letter as the last character of image alt text.
    letters = [image['alt'][-1] for image in images]
    letters = ''.join(letters)

    # Scrape the answers
    # All the answers are found in a <table> with class='bee-set'
    bee_set = soup.find('table', class_='bee-set')
    # Each answer is inside a <td> tag with class = 'bee-hover'
    bee_hover = bee_set.find_all('td', class_='bee-hover')
    # The actual string is the text of the <a> tag.
    answers = [item.a.text for item in bee_hover]

    return date, letters, answers


def main():
    '''
    Scrapes todays answers from sbsolver.com
    '''
    site_url = 'https://www.sbsolver.com/answers'
    file_name = 'answers.html'

    # Download the file site locally to avoid hammering the site.
    if not os.path.exists(file_name):
        print(f'{file_name} does not exist, downloading from {site_url}.')
        download(site_url, file_name)

    # Open the downloaded file and scrape it.
    with open(file_name) as file:
        date, letters, answers = scrape(file.read())
    
    # Print the date
    print(f'Puzzle for {date}')

    # Print the letters
    print(f'Letters: {letters}')
    
    # Print the answers
    print(f'{len(answers)} Answers:')
    for word in answers:
        print(word)

if __name__ == '__main__':
    main()