import os

from balderhub.url.lib.utils import Url

import balderhub.django.contrib.crud.scenario_features


class BaseGeneralAdminModelConfig(balderhub.django.contrib.crud.scenario_features.GeneralAdminModelConfig):

    @property
    def admin_root_url(self) -> Url:
        host = os.getenv('SELENIUM_DJANGO_HOSTNAME', 'localhost')
        return Url(f"http://{host}:8000/admin")
