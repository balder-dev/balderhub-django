Utilities
*********

This section shows general objects and helper functions that are used with this package.


Data Environment Mixin
======================

.. autoclass:: balderhub.django.lib.utils.DataEnvironmentForDjangoMixin
    :members:

GUI Elements
============

General Admin HTML Element
--------------------------

.. autoclass:: balderhub.django.lib.utils.gui.admin.BaseFooterContainer
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.BaseHeaderContainer
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.BaseMainContentContainer
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.BreadcrumbsContainer
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.ChangeListCellElement
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.ChangeListColumnHeader
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.ChangeListFilter
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.ChangeListFilterSidebar
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.ChangeListResultRow
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.ChangeListResultTable
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.DefaultAdminHeaderContainer
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.HtmlSelect2GlobalList
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.MainModuleContainer
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.ChangeFormContainer
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.ChangeFormFieldset
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.ChangeFormSubmitRow
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.MessageElement
    :members:

Admin HTML Widgets
------------------

.. autoclass:: balderhub.django.lib.utils.gui.admin.widgets.HtmlSelect2AutocompleteSelect
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.widgets.ManyToManySelectorWidget
    :members:

Admin Change-Form-Fields HTML Element
-------------------------------------

.. autoclass:: balderhub.django.lib.utils.gui.admin.change_form_fields.BaseChangeFormField
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.change_form_fields.DateChangeFormField
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.change_form_fields.ForeignKeyChangeFormField
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.change_form_fields.InputChangeFormField
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.change_form_fields.M2MChangeFormField
    :members:

.. autoclass:: balderhub.django.lib.utils.gui.admin.change_form_fields.TextareaChangeFormField
    :members:

Response-Messages
=================


.. autoclass:: balderhub.django.lib.utils.response_messages.AdminFieldErrorMessage
    :members:


.. autoclass:: balderhub.django.lib.utils.response_messages.AdminGlobalErrorNote
    :members:


.. autoclass:: balderhub.django.lib.utils.response_messages.AdminGlobalMessage
    :members:

Utility Functions
=================

.. autofunction:: balderhub.django.lib.utils.functions.parse_datetime_according_formats

.. autofunction:: balderhub.django.lib.utils.functions.parse_date_according_formats

.. autofunction:: balderhub.django.lib.utils.functions.get_django_field_names_from_html_class_attribute