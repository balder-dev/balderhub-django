from typing import Union, List

from balderhub.url.lib.utils import Url

from balderhub.django.contrib.crud.scenario_features import GeneralAdminModelConfig

from balderhub.django.lib.pages.admin.change_list_page import ChangeListPage


class AutoChangeListPage(ChangeListPage):
    """
    Represents an admin change list page in a Django-based application.

    This class provides functionality to interact with the admin change list page
    and navigate to it dynamically based on the application and model names.
    """
    # main configuration object for the admin model. It provides details such as the root URL, app and model name
    admin_config = GeneralAdminModelConfig()

    @property
    def applicable_on_url_schema(self) -> Union[Url, List[Url]]:
        return Url(self.admin_config.admin_root_url.as_string() + '/<str:app>/<str:model>')

    def open(self):
        """
        Opens the URL specified by the applicable URL schema.

        The method utilizes the stored URL schema to navigate to the target
        location using the associated driver. The navigation process is
        expected to adhere to the format and structure defined in the
        URL schema.
        """
        self.driver.navigate_to(
            self.applicable_on_url_schema.fill_parameters(
                app=self.admin_config.app_name,
                model=self.admin_config.model_name
            ).as_string()
        )
