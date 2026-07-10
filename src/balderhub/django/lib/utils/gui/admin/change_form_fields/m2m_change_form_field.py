from balderhub.html.lib.utils import Selector
import balderhub.html.lib.utils.components as html
from .base_change_form_field import BaseChangeFormField
from ..widgets.many_to_many_selector_widget import ManyToManySelectorWidget


class M2MChangeFormField(BaseChangeFormField):
    """Field container for many-to-many selector fields in a Django admin change form."""

    @property
    def label(self):
        """Returns the label element for this field."""
        # TODO optimize
        # workaround for django 6: label is placed on higher element:
        #  <div class="form-row field-categories">
        #   <fieldset aria-describedby="id_categories_helptext">
        #       <legend for="id_categories">Categories:</legend>
        #       <div>
        #           <div class="flex-container">
        #               <div class="related-widget-wrapper" data-model-ref="category">
        #                   <div class="selector">
        #                       <div class="selector-available">
        #                           ...
        #                       </div>
        #                       <ul class="selector-chooser">
        #                           ...
        #                       </ul>
        #                       <div id="id_categories_selector_chosen" class="selector-chosen">
        #                           ...
        #                       </div>
        #                       ...
        #                   </div>
        #               </div>
        #           </div>
        #       </div>
        #  </fieldset>
        # </div>
        legend = html.HtmlElement.by_selector(self.driver, Selector.by_xpath('../../legend'), parent=self)
        if legend.exists():
            return legend
        return super().label

    @property
    def field(self) -> ManyToManySelectorWidget:
        """Returns the many-to-many selector widget element."""
        return ManyToManySelectorWidget.by_selector(
            self.driver, Selector.by_css('.related-widget-wrapper .selector'), parent=self
        )

    @property
    def btn_add(self) -> html.HtmlAnchorElement:
        """Returns the 'Add related' anchor link element."""
        return html.HtmlAnchorElement.by_selector(
            self.driver, Selector.by_css('.related-widget-wrapper-link.add-related'), parent=self
        )
