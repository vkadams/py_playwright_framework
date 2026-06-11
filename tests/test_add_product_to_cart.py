'''
Test Case: Add Product to Cart

===================================================
Test Steps
===================================================
1. Open the application in the browser.
2. Locate the Search box on the Homepage.
3. Enter valid product name and click the Search button.
4. Verify that the search results page displays products matching the entered name.
5. Select the desired product from the list.
6. On the product page, update the product quantity (e.g.,2).
7. Click on the "Add to Cart" button.
8. Verify that a success confirmation message is displayed indicating
    the product has been successfully added to the cart.

Expected Results:
_________________
The product should be successfully added to the cart,
and visible confirmation message should appear.
'''

import pytest
import time
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from config import Config

@pytest.mark.regression
def test_add_product_to_cart(page):

    # we are getting test data from Config
    product_name = Config.product_name
    quantity = Config.product_quantity

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Search for a product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    # Select product from product list
    product_page = search_results_page.select_product(product_name)
    time.sleep(2)

    # set quantity & add to cart
    product_page.set_quantity(quantity)
    product_page.add_to_cart()
    time.sleep(2)

    # verify confirmation message
    expect(product_page.get_confirmation_message()).to_be_visible(timeout=3000)
