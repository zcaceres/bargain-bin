from pyramid.view import view_config
from bargain_bin.infrastructure import abebooks_scraper as scraper

PROJECT_NAME = "The Bargain Bin"

# Constant strings for paths passed in view below
AUTHOR = 'author'
TITLE = 'title'
IMG_URL = 'img_url'
YEAR = 'year'
PRICE = 'price'
SHIPPING = 'shipping'
DESCRIPTION = 'description'
URL = 'url'


"""
    Pyramid Noob notes for Zach:
        This controller returns any data (or I guess behaviour too) that needs to be called when the view is loaded.

        The route is hooked up so that request delivers the proper template. The route name is what is called in
        config.add_route and the HTML to render is passed as renderer. The init.main() method add_route ties
        together the homepage (route name) and the url request (/homepage)
"""


@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    book = scraper.scrape_abebooks()

    return {'project': PROJECT_NAME, TITLE: book.title, IMG_URL: book.img_url,
            YEAR: book.year, AUTHOR: book.author, PRICE: book.price,
            SHIPPING: book.shipping, DESCRIPTION: book.desc, URL: book.url}
