'''
Test Case: User Login Functionality

===========================================
Test Steps
===========================================
Test Case 1: Verify login with Invalid Credentials
__________________________________________________
1. Open the application in the browser.
2. Navigate to the "My Account" menu on the Home page.
3. Click on the "Login" link.
4. Enter an invalid email address and password.
5. Click on the "Login" button.
6. Verify that an error message appears indicating invalid credentials.

Expected Results:
-----------------
An error messsage should be displayed, and the user should not be logged in.


Test Case 2: Verify login with Valid Credentials
__________________________________________________
1. Open the application in the browser.
2. Navigate to the "My Account" menu on the Home page.
3. Click on the "Login" link.
4. Enter a valid email address and password.
5. Click on the "Login" button.
6. Verify that "My Account" page is displayed after successful login.

Expected Results:
-----------------
The "My Account" page should appear, confirming successful login.
'''
import time

import pytest

'''
we need homepage for to click on login link
login page to enter credentials
if success, then we land on account page
totally 3 pages needs to be imported
'''
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from playwright.sync_api import expect
from config import Config # for test data

@pytest.mark.sanity
def test_invalid_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    # entering credentials
    login_page.set_email(Config.invalid_email)
    login_page.set_password(Config.invlaid_password)
    login_page.click_login()
    time.sleep(3)

    # we are going to get error
    #login_page.get_login_error() # this is locator
    expect(login_page.get_login_error()).to_be_visible(timeout=3000)


def test_valid_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    # entering credentials
    login_page.set_email(Config.email)
    login_page.set_password(Config.password)
    login_page.click_login()
    time.sleep(3)

    # since login will be successful, we will see my account page
    #my_account_page.get_my_account_page_heading() # locator
    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=3000)

