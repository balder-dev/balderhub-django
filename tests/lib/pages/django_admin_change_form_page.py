import os

from balderhub.django.lib.pages.admin.change_form_page import ChangeFormPage
from balderhub.url.lib.utils import Url


class DjangoAdminChangeFormPage(ChangeFormPage):

    @property
    def applicable_on_url_schema(self) -> Url:
        host = os.getenv('SELENIUM_DJANGO_HOSTNAME', 'localhost')
        # typical change form URL in Django admin: /admin/<app>/<model>/<object_id>/change/
        # also for adding new objects: /admin/<app>/<model>/add/
        return Url(f"http://{host}:8000/admin/<str:app>/<str:model>/<str:object_id>/change/")

    def open(self, app: str, model: str, object_id: str):
        self.driver.navigate_to(self.applicable_on_url_schema.fill_parameters(app=app, model=model, object_id=object_id))
