from typing import Union, List

import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector
from balderhub.url.lib.utils import Url

from balderhub.django.lib.utils.gui.admin import BaseMainContentContainer, DefaultAdminHeaderContainer, \
    ChangeListResultTable, ChangeListFilterSidebar, BreadcrumbsContainer

from .base_django_admin_page import BaseDjangoAdminPage


class ChangeListPage(BaseDjangoAdminPage):
    """
    Page object representing a Django admin change list page for listing model instances.

    This page is implemented according the following structure:

    .. image:: _static/balderhub_django_changelist.png
        :align: center
    """

    class InnerContent(BaseMainContentContainer):
        """Inner content container of the change list page."""

        @property
        def input_search(self) -> html.HtmlElement:
            """Returns the search input element."""
            return html.HtmlElement.by_selector(self.driver, Selector.by_id('searchbar'), parent=self)

        @property
        def btn_search(self) -> html.HtmlElement:
            """Returns the search submit button element."""
            return html.HtmlElement.by_selector(
                self.driver, Selector.by_css('#changelist-search input[type="submit"]'), parent=self
            )

        @property
        def select_action(self) -> html.HtmlSelectElement:
            """Returns the action select dropdown element."""
            return html.HtmlSelectElement.by_selector(self.driver, Selector.by_name('action'), parent=self)

        @property
        def btn_action_go(self) -> html.HtmlButtonElement:
            """Returns the 'Go' button element for executing the selected action."""
            return html.HtmlButtonElement.by_selector(
                self.driver, Selector.by_css('.actions button[type="submit"]'), parent=self
            )

        @property
        def result_table(self) -> ChangeListResultTable:
            """Returns the result table containing the listed model instances."""
            return ChangeListResultTable.by_selector(self.driver, Selector.by_id('result_list'), parent=self)

        @property
        def filter_sidebar(self) -> ChangeListFilterSidebar:
            """Returns the filter sidebar container."""
            return ChangeListFilterSidebar.by_selector(self.driver, Selector.by_id('changelist-filter'), parent=self)

        @property
        def span_result_count(self) -> html.HtmlSpanElement:
            """Returns the span element displaying the result count."""
            return html.HtmlSpanElement.by_selector(self.driver, Selector.by_class('paginator'), parent=self)

    @property
    def applicable_on_url_schema(self) -> Union[Url, List[Url]]:
        raise NotImplementedError

    @property
    def header(self) -> DefaultAdminHeaderContainer:
        """Returns the admin header container."""
        return DefaultAdminHeaderContainer.by_selector(self.driver, Selector.by_tag('header'))

    @property
    def content(self) -> InnerContent:
        """Returns the inner content container of the change list page."""
        return self.InnerContent.by_selector(self.driver, Selector.by_class('content'))

    @property
    def breadcrumbs(self) -> BreadcrumbsContainer:
        """Returns the breadcrumbs navigation container."""
        return BreadcrumbsContainer.by_selector(self.driver, Selector.by_class('breadcrumbs'))

    @property
    def btn_add(self) -> html.HtmlAnchorElement:
        """Returns the 'Add' button anchor element for creating a new model instance."""
        return html.HtmlAnchorElement.by_selector(self.driver, Selector.by_class('addlink'))
