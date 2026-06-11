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

# load test data from the files
from utils.data_reader_util import read_csv_data, read_json_data, read_excel_data
csv_data = read_csv_data(r"C:\Users\61015706\OneDrive - LTIMindtree\Documents\PY\PY_Framework\testdata\logindata.csv")
json_data = read_json_data(r"C:\Users\61015706\OneDrive - LTIMindtree\Documents\PY\PY_Framework\testdata\logindata.json")
excel_data = read_excel_data(r"C:\Users\61015706\OneDrive - LTIMindtree\Documents\PY\PY_Framework\testdata\logindata.xlsx")

@pytest.mark.datadriven
@pytest.mark.parametrize('testName,email,password,expected', csv_data)
def test_login_data_driven_csv(page,testName,email,password,expected):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    # entering credentials
    login_page.login(email,password)
    time.sleep(3)

    # there are 2 scenarios-- valid & invalid
    if expected == "success":
        expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=3000)
    else:
        expect(login_page.get_login_error()).to_be_visible(timeout=3000)

@pytest.mark.parametrize('testName,email,password,expected', json_data)
def test_login_data_driven_json(page,testName,email,password,expected):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    # entering credentials
    login_page.login(email,password)
    time.sleep(3)

    # there are 2 scenarios-- valid & invalid
    if expected == "success":
        expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=3000)
    else:
        expect(login_page.get_login_error()).to_be_visible(timeout=3000)


@pytest.mark.parametrize('testName,email,password,expected', excel_data)
def test_login_data_driven_excel(page,testName,email,password,expected):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    # entering credentials
    login_page.login(email,password)
    time.sleep(3)

    # there are 2 scenarios-- valid & invalid
    if expected == "success":
        expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=3000)
    else:
        expect(login_page.get_login_error()).to_be_visible(timeout=3000)
