from playwright.sync_api import Page

class RegisterationPage:
    '''
    Page Object Model class for 'Registeration' Page.
    This class contains web element locators and methods (actions)
    to interact with the registration form.
    '''
    def __init__(self, page: Page):
        self.page = page

        #===locators===
        # Input fields
        self.txt_firstname = self.page.get_by_role('textbox', name='First Name') # Rajeev
        self.txt_lastname = self.page.get_by_role('textbox', name='Last Name') # Bhai
        self.txt_email = self.page.get_by_role('textbox', name='E-Mail') # rajeev.bro@superdevs.com/rajeev.bro22@superdevs.com
        self.txt_telephone = self.page.get_by_role('textbox', name='Telephone') # 8347328479
        self.txt_password = self.page.get_by_label('Password', exact=True) # test@123
        self.txt_confirm_password = self.page.get_by_role('textbox', name='Password Confirm') # test@123

        # Checkbox & buttons
        self.chk_policy = self.page.get_by_role('checkbox')
        self.btn_continue = self.page.locator('input[value="Continue"]')

        # confirmation message
        self.confirmation_message = self.page.locator("div[id='content'] h1")

        # === Action methods ===
    def set_first_name(self, fname):
        self.txt_firstname.fill(fname)

    def set_last_name(self, lname):
        self.txt_lastname.fill(lname)

    def set_email(self, email):
        self.txt_email.fill(email)

    def set_telephone(self, tel):
        self.txt_telephone.fill(tel)

    def set_password(self, pwd):
        self.txt_password.fill(pwd)

    def set_confirm_password(self, pwd):
        self.txt_confirm_password.fill(pwd)

    def set_privacy_policy(self):
        self.chk_policy.check()

    def click_continue(self):
        self.btn_continue.click()

    def get_confirmation_message(self):
        '''
        return the confirmation message locator
        this can be used to verify successful registration
        '''
        return self.confirmation_message

    # combined
    def complete_registration(self, user_data):
        self.set_first_name(user_data['firstname'])
        self.set_last_name(user_data['lastname'])
        self.set_email(user_data['email'])
        self.set_telephone(user_data['telephone'])
        self.set_password(user_data['password'])
        self.set_confirm_password(user_data['password'])
        self.set_privacy_policy()
        self.btn_continue.click()

        # return confirmation message locator
        return self.confirmation_message
