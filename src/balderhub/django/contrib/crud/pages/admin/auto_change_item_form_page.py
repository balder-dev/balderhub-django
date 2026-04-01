from typing import Union, List

from balderhub.url.lib.utils import Url

from balderhub.django.contrib.crud.scenario_features import GeneralAdminModelConfig

from balderhub.django.lib.pages.admin.change_form_page import ChangeFormPage


class AutoChangeItemFormPage(ChangeFormPage):
    """
    Represents a page for changing an item in the Django admin interface.

    Provides functionality to interact with the Django admin change item page.
    Utilizes a configurable URL schema and navigation method to allow access
    to the relevant page in the admin interface.
    """
    # contains the configuration for the admin model, including app name, model name, and root URL.
    admin_config = GeneralAdminModelConfig()

    @property
    def applicable_on_url_schema(self) -> Union[Url, List[Url]]:
        return Url(self.admin_config.admin_root_url.as_string() + '/<str:app>/<str:model>/<int:id>/change/')

    def open(self, item_id: int):
        """
        Navigates to the URL of a specific item based on the provided item ID. The URL is constructed
        using the application's configuration parameters and the item ID supplied.

        :param item_id: The unique identifier of the item to navigate to.
        """
        self.driver.navigate_to(
            self.applicable_on_url_schema.fill_parameters(
                app=self.admin_config.app_name,
                model=self.admin_config.model_name,
                id=item_id
            ).as_string()
        )
