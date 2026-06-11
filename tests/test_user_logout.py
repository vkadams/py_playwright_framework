'''
Test Case: User Logout Functionality

===================================================
Test Steps
===================================================
1. Open the application in the browser.
2. Navigate to the "My Account" menu and click on "login".
3. Enter valid user credentials (email and password).
4. Click on the "Login" button.
5. Verify that the "My Account" page is displayed
6. Click on the "Logout" link/button.
7. Verify that the Logout confirmation page is displayed.
8. Click on the "Continue" button to return to the Homepage.
9. Verify that Homepage is displayed by checking its title.

Expected Results:
_________________
After logging out, the user should be redirected to the Logout confirmation page.
Clicking continue, should navigate back to Homepage successfully.
'''

import pytest
import time
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from config import Config

@pytest.mark.regression
def test_user_logout(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    # navingate to login page
    home_page.click_my_account()
    home_page.click_login()

    # enter valid credentials
    login_page.set_email(Config.email)
    login_page.set_password(Config.password)
    login_page.click_login()

    # verify my account page is displayed
    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=3000)

    # perform logout action
    logout_page = my_account_page.click_logout() # this will return logout page & this is nothing but chaining of methods

    # verify logout page is displayed-- continue button
    expect(logout_page.get_continue_button()).to_be_visible(timeout=3000)

    # click on continue button-- to return to Homepage
    logout_page.click_continue()

    # Verify Homepage title is displayed
    expect(page).to_have_title("Your Store")
