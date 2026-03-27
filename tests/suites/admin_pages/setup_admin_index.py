import logging
import os
import time

import balder

from tests.lib.setup_features.selenium_feature import SeleniumFeature
from tests.lib.pages import DjangoAdminIndexPage, DjangoAdminLoginPage, DjangoAdminChangeListPage, \
    DjangoAdminChangeFormPage

logger = logging.getLogger(__name__)


class SetupAdminIndex(balder.Setup):

    class Server(balder.Device):
        pass

    @balder.connect(Server, over_connection=balder.Connection)
    class Browser(balder.Device):
        selenium = SeleniumFeature()
        login_page = DjangoAdminLoginPage()
        index_page = DjangoAdminIndexPage()
        change_list_page = DjangoAdminChangeListPage()
        change_form_page = DjangoAdminChangeFormPage()

    @balder.fixture('setup')
    def connect_selenium(self):
        self.Browser.selenium.create()
        yield
        self.Browser.selenium.quit()

    @balder.fixture('variation')
    def make_sure_to_be_logged_in(self):
        self.Browser.login_page.open()
        if self.Browser.login_page.is_applicable():
            logger.info('user is not logged in yet - log in user with selenium')
            username = os.getenv('DJANGO_SUPERUSER_USERNAME')
            password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

            self.Browser.login_page.input_username.type_text(username, clean_before=True)
            self.Browser.login_page.input_password.type_text(password, clean_before=True)
            self.Browser.login_page.btn_login.click()
            self.Browser.index_page.wait_for_page()
            logger.info('user is logged in now')
        else:
            # already logged in
            logger.info('user is already logged in - do nothing')
