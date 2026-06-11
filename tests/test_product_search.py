'''
Test Case: Product Search Functionality

===================================================
Test Steps
===================================================
1. Open the application in the browser.
2. Locate the search box on the Home page.
3. Enter a valid product name in the search box.
4. Click on the "search" button
5. Verify that the Search Results page is displayed
6. Check if searched product name appears in the list of search results.

Expected Results:
_________________
The search results page should appear, and the searched product should be
visible in the search result list.

we will need PO classes-- Homepage-- we have search box, search results page
'''
import time

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
# we need to read product name from config.py
from config import Config

@pytest.mark.sanity
@pytest.mark.regression
def test_product_search(page):
    product_name = Config.product_name
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    home_page.enter_product_name(product_name)
    home_page.click_search()
    time.sleep(2)

    expect(search_results_page.get_search_results_page_header()).to_be_visible(timeout=3000)
    # check if product is in the list
    expect(search_results_page.is_product_exist(product_name)).to_be_visible(timeout=3000)



