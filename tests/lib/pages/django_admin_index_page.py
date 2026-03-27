import os

from balderhub.django.lib.pages.admin.index_page import IndexPage
from balderhub.url.lib.utils import Url


class DjangoAdminIndexPage(IndexPage):

    @property
    def applicable_on_url_schema(self) -> Url:
        host = os.getenv('DJANGO_HOSTNAME', 'localhost')
        return Url(f"http://{host}:8000/admin/")

    def open(self):
        self.driver.navigate_to(self.applicable_on_url_schema)
