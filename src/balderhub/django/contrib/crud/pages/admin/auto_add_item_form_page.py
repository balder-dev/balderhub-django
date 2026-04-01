from typing import Union, List

from balderhub.url.lib.utils import Url

from balderhub.django.contrib.crud.scenario_features import GeneralAdminModelConfig

from balderhub.django.lib.pages.admin.change_form_page import ChangeFormPage


class AutoAddItemFormPage(ChangeFormPage):
    """
    Represents a page for adding an item via the Django admin interface.

    This class models the behavior and attributes relevant for an admin page where
    items can be added. It is specifically designed to integrate with Balderhub's
    Django utilities and manage navigation to the appropriate admin URL for adding
    new items.
    """
    #: main configuration object containing information about the admin panel, such as root URL, app and model name
    admin_config = GeneralAdminModelConfig()

    @property
    def applicable_on_url_schema(self) -> Union[Url, List[Url]]:
        return Url(self.admin_config.admin_root_url.as_string() + '/<str:app>/<str:model>/add')

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
