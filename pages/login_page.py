from playwright.sync_api import Page, Playwright

class LoginPage:
    ''' Page Object Model class for login page. '''
    def __init__(self, page: Page):
        self.page = page
        '''
        constructor that initializes the playwright page instance
        and defines all locators on the login page
        '''
        self.txt_email_address = self.page.get_by_role('textbox', name='E-Mail Address')
        self.txt_password = self.page.get_by_role('textbox', name='Password')
        self.btn_login = self.page.locator('input[value="Login"]')
        self.txt_error_message = self.page.get_by_text('Warning: No match for E-Mail Address and/or Password.')


    # action methods
    # these methods represent user interaction on login page
    def set_email(self, email):
        try:
            self.txt_email_address.fill(email)
        except Exception as e:
            print(f'Exception while entering email address: {e}')
            raise

    def set_password(self, password):
        try:
            self.txt_password.fill(password)
        except Exception as e:
            print(f'Exception while entering password: {e}')
            raise

    def click_login(self):
        try:
            self.btn_login.click()
        except Exception as e:
            print(f'Exception while clicking login button: {e}')
            raise


    def login(self, email, password):
        '''
        perform complete login operation
        Enter email
        Enter password
        click login button
        '''
        self.set_email(email)
        self.set_password(password)
        self.click_login()

    def get_login_error(self):
        '''
        return the error message if login fails.
        Example use:
            error_text = login_page.get_login_error().inner_text()
        '''
        try:
            return self.txt_error_message
        except Exception as e:
            print(f'Exception while getting error message: {e}')
            return None
