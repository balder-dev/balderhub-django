from typing import Union, List

import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector
from balderhub.url.lib.utils import Url

from balderhub.django.lib.utils.gui.admin import BaseMainContentContainer, DefaultAdminHeaderContainer, \
    BreadcrumbsContainer, ChangeFormContainer

from .base_django_admin_page import BaseDjangoAdminPage


class ChangeFormPage(BaseDjangoAdminPage):
    """
    Page object representing a Django admin change form page for editing a single model instance.

    This page is implemented according the following structure:

    .. image:: _static/balderhub_django_changeform.png
        :align: center
    """

    class InnerContent(BaseMainContentContainer):
        """Inner content container of the change form page."""

        @property
        def h1_title(self) -> html.HtmlElement:
            """Returns the main title heading element."""
            return html.HtmlElement.by_selector(self.driver, Selector.by_tag('h1'), parent=self)

        @property
        def h2_caption(self) -> html.HtmlElement:
            """Returns the caption heading element."""
            return html.HtmlElement.by_selector(self.driver, Selector.by_tag('h2'), parent=self)

        @property
        def form(self) -> ChangeFormContainer:
            """Returns the change form container element."""
            # typical django change-form id follows [modelname]_form but it always has class 'change-form'
            # since we don't know the model name here, we can use the class
            return ChangeFormContainer.by_selector(self.driver, Selector.by_tag('form'), parent=self)

        @property
        def object_tools(self) -> html.HtmlLiElement:
            """Returns the object tools list element."""
            return html.HtmlLiElement.by_selector(self.driver, Selector.by_class('object-tools'), parent=self)

    @property
    def applicable_on_url_schema(self) -> Union[Url, List[Url]]:
        raise NotImplementedError

    @property
    def header(self) -> DefaultAdminHeaderContainer:
        """Returns the admin header container."""
        return DefaultAdminHeaderContainer.by_selector(self.driver, Selector.by_tag('header'))

    @property
    def content(self) -> InnerContent:
        """Returns the inner content container of the change form page."""
        return self.InnerContent.by_selector(self.driver, Selector.by_class('content'))

    @property
    def breadcrumbs(self) -> BreadcrumbsContainer:
        """Returns the breadcrumbs navigation container."""
        return BreadcrumbsContainer.by_selector(self.driver, Selector.by_class('breadcrumbs'))
