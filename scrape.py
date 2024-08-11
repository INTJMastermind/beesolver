import requests
import os
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
    soup = BeautifulSoup(site, 'lxml')
    return [td.a.text for td in soup.find_all('td', class_='bee-hover')]


def main():
    site_url = 'https://www.sbsolver.com/answers'
    file_name = 'answers.html'
    # Download the file site locally to avoid hammering the site.
    if not os.path.exists(file_name):
        print(f'{file_name} does not exist, downloading from {site_url}.')
        download(site_url, file_name)

    # Open the downloaded file and scrape it.
    with open(file_name) as file:
        answers = scrape(file.read())
    
    # Print the answers
    for a in answers:
        print(a)

if __name__ == '__main__':
    main()