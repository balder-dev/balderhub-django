import os

from balderhub.django.lib.pages.admin.login_page import LoginPage
from balderhub.url.lib.utils import Url


class DjangoAdminLoginPage(LoginPage):

    @property
    def applicable_on_url_schema(self) -> Url:
        host = os.getenv('SELENIUM_DJANGO_HOSTNAME', 'localhost')
        # Django admin login is usually at /admin/login/
        return Url(f"http://{host}:8000/admin/login/")

    def open(self):
        self.driver.navigate_to(self.applicable_on_url_schema)
