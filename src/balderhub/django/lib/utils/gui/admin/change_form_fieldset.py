import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector

from balderhub.django.lib.utils.gui.admin.change_form_fieldset_row import ChangeFormFieldsetRow


class ChangeFormFieldset(html.HtmlElement):
    """Container representing a single fieldset within a Django admin change form."""

    def get_all_rows(self) -> list[ChangeFormFieldsetRow]:
        """Returns a list of all form rows within this fieldset."""
        bridges = self.bridge.find_bridges(Selector.by_class('form-row'))
        return [ChangeFormFieldsetRow(bridge) for bridge in bridges]
