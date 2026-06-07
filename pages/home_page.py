from playwright.sync_api import Page, Playwright

class HomePage(Page):
    ''' Page Object Model class for 'Home' Page. '''
    def __init__(self, page: Page):
        '''
        Constructor to initialize the Playwright Page Object
        and define all necessary locators
        '''
        self.page = page

        #===locators===
        self.lnk_my_account = self.page.locator('span:has-text("My Account")')
        self.lnk_register = self.page.get_by_role('link',name='Register')
        self.lnk_login = self.page.get_by_role('link',name='Login')
        self.txt_search_box = self.page.get_by_role('textbox',name='Search')
        self.btn_search = self.page.locator('button[class="btn btn-default btn-lg"]')


    # action methods
    # each method represents user interaction on the page

    def get_home_page_title(self):
        ''' Return the title of Home page'''
        title = self.page.title()
        return title

    def click_my_account(self):
        ''' Click My Account link'''
        try:
            self.lnk_my_account.click()
        except Exception as e:
            print(f'Exception while clicking on my account: {e}')
            raise

    def click_register(self):
        '''Click on register link under my account'''
        try:
            self.lnk_register.click()
        except Exception as e:
            print(f'Exception while clicking Register: {e}')
            raise

    def click_login(self):
        ''' click on login link under my account'''
        try:
            self.lnk_login.click()
        except Exception as e:
            print(f'Exception while clicking Login: {e}')
            raise

    def enter_product_name(self, product_name):
        '''Enter the product name into search input box'''
        try:
            self.txt_search_box.fill(product_name)
        except Exception as e:
            print(f'Exception while entering product name: {e}')
            raise

    def click_search(self):
        ''' click on search button to initiate search'''
        try:
            self.btn_search.click()
        except Exception as e:
            print(f'Exception while clicking "search" button: {e}')
            raise

        
