"""
    Web Scraping Behaviour for Abebooks.com
"""

from random import randint
from io import FileIO as file
import requests
from bs4 import BeautifulSoup

SEARCH_URL = \
    "https://www.abebooks.com/servlet/SearchResults?bi=0&bx=off&ds=30&" \
    "recentlyadded=all&sortby=17&sts=t&tn="

PATH_TO_NOUN_LIST = "/Users/zachcaceres/PycharmProjects/bargain_bin/bargain_bin/bargain_bin/util/nounlist.txt"


class Book:
    def __init__(self, title, image_url, year, author, price, shipping, description, url):
        self.title = title
        self.img_url = image_url
        self.year = year
        self.author = author
        self.price = price
        self.shipping = shipping
        self.desc = description
        self.url = url


# Method called from view for scrape cycle
def scrape_abebooks():
    query = generate_noun_query()
    search_string = create_search_string(query)
    soup = http_request_and_soup(search_string)
    section, spans, ahrefs, imgs = get_book_sections_from_soup(soup)
    book = get_book_elements_from_soup(section, spans, ahrefs, imgs)
    print("Made a book: {0}".format(book.title))
    return book


# Generates a noun from a list of 4k for searching Abebooks
def generate_noun_query():
    with open(PATH_TO_NOUN_LIST, 'r') as noun_file:
        noun_list = file.readlines(noun_file)
    noun = noun_list[randint(0, len(noun_list))]
    print ('Querying for: {0}'.format(noun))
    return noun


# Concatenates string for search query
def create_search_string(query):
    search_str = SEARCH_URL + "{0}".format(query)
    print ("Search string is: {0}".format(search_str))
    return search_str

# Requests to get soup
def http_request_and_soup(search_string):
    r = requests.get('{0}'.format(search_string))
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_book_sections_from_soup(soup):
    # Get HTML bundles
    try:
        section = soup.find(id="book-1")

        spans = section.find_all("span", limit = 10)

        ahrefs = section.find_all("a", limit = 10)

        imgs = section.find_all("img", limit = 1)

        return section, spans, ahrefs, imgs
    except TypeError:
        print("THERE WAS A TYPE ERROR EXCEPTION getting HTML BUNDLES")
        scrape_abebooks()



"""
    Needs:
        Section to handle when there is an ISBN and YEAR (brook)


        Section for NO ISBN and NO YEAR (abolishment)


        Section for YEAR and NO ISBN (puritan)


        Section for NO YEAR and ISBN (mustard)
            Desc: span 7
            Shipping: span 6
"""


def get_book_elements_from_soup(section, spans, ahrefs, imgs):
    # Get Elements from HTML Bundles
    try:
        has_year = True
        for s in spans:
            print (s)
        title = spans[0].text


        author = section.find_all("p", class_="author")[0].text
        if author == "":
            author = "No author listed"

        # If no year data go unknown, otherwise get from Span[2]
        if spans[2].a or spans[2].has_attr('class'):
            year = "Unknown year"
            has_year = False
        else:
            year = spans[2].text

        if spans[3].a:
            # print("Found an ISBN, going into if statement: {0}".format(spans[2].text))
            if has_year:
                print("Has ISBN and has year is {0}".format(has_year))
                # Handles existence of ISBN but has a year
                shipping = spans[7].text
                description = spans[8].text
            else:
                print("Has ISBN and has year is {0}".format(has_year))
                # Handles Existence of ISBN but no year
                shipping = spans[6].text
                description = spans[7].text

        else:
            # Handles if NO ISBN
            if has_year:
                print("Has no ISBN and has year is {0}".format(has_year))
                shipping = spans[5].text
                description = spans[6].text
            else:
                print("Has no ISBN and has year is {0}".format(has_year))
                shipping = spans[4].text
                description = spans[5].text

        if spans[2].has_attr('class'):
            if spans[2]['class'][0] == 'no-wrap':
               print("GOING INSIDE NO WRAP")
               shipping = spans[4].text
               description = spans[5].text


        price_block = section.select(".price")
        price = price_block[0].text


        if ahrefs[0].has_attr('class'):
            book_url = "https://www.abebooks.com{0}".format(ahrefs[0]['href'])
        else:
            book_url = "https://www.abebooks.com{0}".format(ahrefs[1]['href'])


        img_url = imgs[0]['src']

        print("Title: {0}".format(title))
        print("Author: {0}".format(author))
        print("Year: {0}".format(year))
        print("Price: {0}".format(price))
        print("Shipping: {0}".format(shipping))
        print("URL: {0}".format(book_url))
        print("Description: {0}".format(description))
        print("IMG: {0}".format(img_url))

        book = Book(title, img_url, year, author, price, shipping, description, book_url)
        return book

    except TypeError:
        print("THERE WAS A TYPE ERROR EXCEPTION getting TEXT FROM ELEMENTS")
        scrape_abebooks()


# for testing call scrape_abebooks() here and python abebooks_scraper.py