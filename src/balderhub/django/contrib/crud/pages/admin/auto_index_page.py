from typing import Union, List

from balderhub.url.lib.utils import Url

from balderhub.django.contrib.crud.scenario_features import GeneralAdminModelConfig

from balderhub.django.lib.pages.admin.index_page import IndexPage


class AutoIndexPage(IndexPage):
    """
    Represents the admin index page in the Django admin interface.

    This class is responsible for representing and interacting with the admin
    index page in a web-driven testing environment. It utilizes configurations
    specified in the `GeneralAdminModelConfig` to auto-determine applicable URL
    schema and other information.

    :ivar admin_config: Stores the general admin configuration settings.
    :type admin_config: GeneralAdminModelConfig
    """
    admin_config = GeneralAdminModelConfig()

    @property
    def applicable_on_url_schema(self) -> Union[Url, List[Url]]:
        return self.admin_config.admin_root_url

    def open(self):
        """
        Opens the URL specified by the applicable URL schema.

        The method utilizes the stored URL schema to navigate to the target
        location using the associated driver. The navigation process is
        expected to adhere to the format and structure defined in the
        URL schema.
        """
        self.driver.navigate_to(self.applicable_on_url_schema.as_string())
