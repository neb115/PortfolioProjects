from bs4 import BeautifulSoup
from pathvalidate import is_valid_filename
from pyfiglet import figlet_format
import datetime, requests, sys, csv, random


"""
This program is designed to present users with a random quote scraped from a website and then allow them to save said quote(s) to a csv file
OR append quotes to an existing csv file
"""

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
           "Accept-Encoding":"gzip, deflate",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "DNT":"1",
           "Connection":"close",
           "Upgrade-Insecure-Requests":"1"}

def main():
    greeting()

def quotes(select: str):
    '''
    Makes a request to the 'quotes to scrape' site based on user choice, then generates random quotes.
    '''

    user_page = 'https://quotes.toscrape.com/tag/'+select+'/'
    page = requests.get(user_page, headers=HEADERS)
    soup1 = BeautifulSoup(page.content,'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    quote_data = []
    quote_elements = soup2.find_all('div', class_='quote')
    for quote_element in quote_elements:
        text = quote_element.find('span', class_='text').get_text(strip=True)
        author = quote_element.find('small', class_='author').get_text(strip=True)
        quote_data.append({'quote': text, 'author': author})

    user_quotes = []
    while True:
        rand_quote = random.choice(quote_data)
        user_quotes.append(rand_quote)
        print(f"\n{rand_quote['quote']}\n-{rand_quote['author']}")
        while True:
                user = input("\nWould you another quote? (y/n) ")
                if user == 'y':
                    break
                elif user == 'n':
                    csv_type(user_quotes)
                else:
                    print("Please enter a valid choice.")
                    continue


def new_csv(file_name2: str, l2: list):
    """
    Creates/updates a new csv file from list of quotes generated in the quotes function.
    """

    today = datetime.date.today()
    extension = file_name2 + '.csv'
    with open(extension, 'a', newline='', encoding='UTF8') as file:
        writer = csv.DictWriter(file, fieldnames=['Quote', 'Author', 'Date Added'])

        if file.tell() == 0:
            writer.writeheader()
        for item in l2:
            writer.writerow({'Quote':item['quote'], 'Author':item['author'], 'Date Added':today})
    sys.exit("Success! Your file has been saved. Thank you and have a good one!")


def greeting():
    """
    Greets user and initiates step 1 -- asking/validating
    """

    print(figlet_format("Quote Scraper"))
    print("\nWelcome to the Quotes Scraper App ver1.0!" \
    "\nAbout:" \
    "\nThis application is a fun way to generate a real quote, or several, scraped from a real website! You may also save said quote(s) to a new or existing csv.")
    print("\nPlease choose from one of these categories to generate a quote: \n*love\n*inspirational\n*life\n*humor\n*books\n*friendship")

    while True:
        user = input().strip()
        if user in ['love', 'inspirational', 'life', 'humor', 'books', 'friendship']:
            quotes(user)
        else:
            print("Please enter a valid choice")
            continue

def csv_type(l1: list):
    while True:
        user = input("\nWould you like to save these quotes to a file? Please type 'y' to proceed, or quit the program with 'q'. ")
        if user == 'y':
            while True:
                file_name = input("\nWhat would you like to name your file? If you would like to update an existing one, please type the name of the file (without the file extension). ")
                file_name = file_name.strip()
                if is_valid_filename(file_name):
                    new_csv(file_name, l1)
                else:
                    print("Please enter a valid file name")
                    continue
        elif user == 'q':
            sys.exit("\nThank you and have a good one!")
        else:
            print("Sorry! Please enter a valid input")
            continue



if __name__ == "__main__":
    main()
