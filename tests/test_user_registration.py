'''
Test Case: User Registration Functionality

===========================================
Test Steps
===========================================
1. Open the application in the browser.
2. Navigate to the "My Account" menu and click on "Register"
3. Enter user details:
    - first name
    - last name
    - email address
    - phone number
    - password & confirm password
4. Accept the privacy policy check box.
5. Click on 'continue' button
6. Verify that the account creation confirmation message is displayed.

Expected Result:
---------------
After submitting valid details, the system should display the message:
"Your Account Has Been Created!"
'''
import pytest
from playwright.sync_api import expect

# import page object classes
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.random_data_util import RandomDataUtil

@pytest.mark.sanity
@pytest.mark.regression
def test_user_registration(page): # this is not playwright page fixture, but this is from conftest.py
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    # click on my account
    home_page.click_my_account()
    # click on register link
    home_page.click_register()

    # using Faker library we will refer to util class
    random_data = RandomDataUtil()
    # fill the form
    registration_page.set_first_name(random_data.get_first_name())
    registration_page.set_last_name(random_data.get_last_name())
    registration_page.set_email(random_data.get_email())
    registration_page.set_telephone(random_data.get_phone_number())
    password= random_data.get_password()
    registration_page.set_password(password)
    registration_page.set_confirm_password(password)

    registration_page.set_privacy_policy()
    registration_page.click_continue()

    # verification
    conf_message = registration_page.get_confirmation_msg()
    expect(conf_message).to_have_text("Your Account Has Been Created!")

