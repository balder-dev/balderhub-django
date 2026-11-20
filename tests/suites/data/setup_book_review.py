import os
import logging

import balder
import balderhub.crud.lib.setup_features.factories
import balderhub.data.lib.setup_features.factories
import balderhub.django.contrib.crud.pages.admin
import balderhub.django.contrib.crud.setup_features
from tests.lib.setup_features.basic_data_environment_feature import BasicDataEnvironmentFeature
from tests.lib.setup_features.data import book_review
from tests.lib.setup_features.selenium_feature import SeleniumFeature
from tests.lib.pages import DjangoAdminIndexPage, DjangoAdminLoginPage
from tests.lib.utils.data import BookReviewDataItem

logger = logging.getLogger(__name__)


class SetupBookReview(balder.Setup):
    # TODO use base class for this!!

    class Server(balder.Device):
        env = BasicDataEnvironmentFeature()
        initial_data = balderhub.data.lib.setup_features.factories.AutoInitialDataConfigFactory.get_for(BookReviewDataItem)()

    @balder.connect(Server, over_connection=balder.Connection)
    class SuperuserClient(balder.Device):

        admin_model_config = book_review.GeneralAdminModelConfig()
        example_create = book_review.CreateExampleProvider()
        example_update = book_review.UpdateFieldExampleProvider()
        example_single_read = balderhub.crud.lib.setup_features.factories.AutoSingleReadExampleFactory.get_for(BookReviewDataItem)()
        selenium = SeleniumFeature()

        login_page = DjangoAdminLoginPage()
        index_page = DjangoAdminIndexPage()
        page_add = balderhub.django.contrib.crud.pages.admin.AutoAddItemFormPage()
        page_update = balderhub.django.contrib.crud.pages.admin.AutoChangeItemFormPage()
        page_list = balderhub.django.contrib.crud.pages.admin.AutoChangeListPage()

        multiple_reader = balderhub.django.contrib.crud.setup_features.factories.AutoAdminMultipleReaderFactory.get_for(BookReviewDataItem)()
        #single_reader = balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleReaderFactory.get_for(BookReviewDataItem)()
        single_creator = balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleCreatorFactory.get_for(BookReviewDataItem)()
        # single_updater = balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleUpdaterFactory.get_for(BookReviewDataItem)()

        multiple_data_with_auth = balderhub.data.lib.setup_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(BookReviewDataItem)(Master="Server")

    @balder.fixture('setup')
    def connect_selenium(self):
        self.SuperuserClient.selenium.create()
        yield
        self.SuperuserClient.selenium.quit()

    @balder.fixture('variation')
    def make_sure_to_be_logged_in(self):
        self.SuperuserClient.login_page.open()
        if self.SuperuserClient.login_page.is_applicable():
            logger.info('user is not logged in yet - log in user with selenium')
            username = os.getenv('DJANGO_SUPERUSER_USERNAME')
            password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

            self.SuperuserClient.login_page.input_username.type_text(username, clean_before=True)
            self.SuperuserClient.login_page.input_password.type_text(password, clean_before=True)
            self.SuperuserClient.login_page.btn_login.click()
            self.SuperuserClient.index_page.wait_for_page()
            logger.info('user is logged in now')
        else:
            # already logged in
            logger.info('user is already logged in - do nothing')
