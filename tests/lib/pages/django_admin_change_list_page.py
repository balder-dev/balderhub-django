import os

from balderhub.django.lib.pages.admin.change_list_page import ChangeListPage
from balderhub.url.lib.utils import Url


class DjangoAdminChangeListPage(ChangeListPage):

    @property
    def applicable_on_url_schema(self) -> Url:
        host = os.getenv('SELENIUM_DJANGO_HOSTNAME', 'localhost')
        return Url(f"http://{host}:8000/admin/<str:app>/<str:model>/")

    def open(self, app: str, model: str):
        self.driver.navigate_to(self.applicable_on_url_schema.fill_parameters(app=app, model=model))
