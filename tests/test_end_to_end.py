'''
End to End flow
1. Register as a new user.
2. Logout
3. Login with registered credentials.
4. Search and add product to cart.
5. Verify cart contents.
'''
import time
import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from config import Config
from pages.shopping_cart_page import ShoppingCartPage
from utils.random_data_util import RandomDataUtil

@pytest.mark.end_to_end
def test_end_to_end_flow(page):
    # step 1: Register new account and capture the generated email.
    registered_email, registered_password = perform_registration(page)
    print("Registration Completed Successfully!")

    # step 2: Logout after registration.
    perform_logout(page)
    print("Logout Completed Successfully!")

    # step 3: Login with registered credentials
    perform_login(page, registered_email, registered_password)
    print("Login Completed Successfully!")

    # step 4: Search product and add to cart
    add_product_to_cart(page)
    print("Product Added to Cart Successfully!")

    # step 5: Verify cart details
    verify_shopping_cart(page)
    print("Shopping Cart Verification Completed!")



# ==============================
# Helper function - Registration
# ==============================
def perform_registration(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    random_data = RandomDataUtil()
    first_name = random_data.get_first_name()
    last_name = random_data.get_last_name()
    email = random_data.get_email()
    password = random_data.get_password()
    phone_number = random_data.get_phone_number()

    registration_page.set_first_name(first_name)
    registration_page.set_last_name(last_name)
    registration_page.set_email(email)
    registration_page.set_telephone(phone_number)
    registration_page.set_password(password)
    registration_page.set_confirm_password(password)
    registration_page.set_privacy_policy()
    registration_page.click_continue()

    expect(registration_page.get_confirmation_msg()).to_have_text("Your Account Has Been Created!")
    return email, password

# ==============================
# Helper function - Logout
# ==============================
def perform_logout(page):
    my_account = MyAccountPage(page)
    logout_page = LogoutPage(page)

    my_account.click_logout()
    expect(logout_page.get_continue_button()).to_be_visible(timeout=3000)
    logout_page.click_continue()
    expect(page).to_have_title("Your Store")


# ==============================
# Helper function - Login
# ==============================
def perform_login(page, email, password):
    home_page = HomePage(page)
    home_page.click_my_account()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.login(email, password)

    my_account = MyAccountPage(page)
    expect(my_account.get_my_account_page_heading()).to_be_visible(timeout=3000)

# ==============================
# Helper function - Search and Add Product to Cart
# ==============================
def add_product_to_cart(page):
    product_name = Config.product_name
    quantity = Config.product_quantity

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    home_page.enter_product_name(product_name)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible(timeout=3000)
    expect(search_results_page.is_product_exist(product_name)).to_be_visible(timeout=3000)

    product_page = search_results_page.select_product(product_name)
    product_page.set_quantity(quantity)
    product_page.add_to_cart()

    expect(product_page.get_confirmation_message()).to_be_visible(timeout=3000)

# ==============================
# Helper function - Verify Shopping Cart
# ==============================
def verify_shopping_cart(page):
    product_page = ProductPage(page)
    product_page.click_items_to_navigate_to_cart()

    shopping_cart_page = product_page.click_view_cart()
    config = Config()
    print("Navigating to Shopping Cart")

    expect(shopping_cart_page.get_total_price()).to_have_text(Config.total_price)