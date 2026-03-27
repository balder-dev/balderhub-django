import os

import balderhub.html.lib.utils.components.inputs
from balderhub.html.lib.scenario_features import HtmlPage
from balderhub.url.lib.utils import Url
from balderhub.html.lib.utils import Selector


class DjangoWelcomePage(HtmlPage):

    @property
    def applicable_on_url_schema(self) -> Url:
        host = os.getenv('DJANGO_HOSTNAME', 'localhost')
        return Url(f"http://{host}:8000/")

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def h1_title(self):
        return balderhub.html.lib.utils.components.HtmlElement.by_selector(self.driver, Selector.by_tag('h1'))

    def open(self):
        self.driver.navigate_to(self.applicable_on_url_schema)
