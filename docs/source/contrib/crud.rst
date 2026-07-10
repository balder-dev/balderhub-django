Contrib for ``balderhub-crud``
******************************

For activating this module, you need to install the package like shown below

.. code-block:: none

    >>> pip install balderhub-django[crud]

Once installed you can use it.

CRUD Feature / Pages Integration
================================

This contribution module connects the generic CRUD testing framework of ``balderhub-crud`` with the Django admin
interface. It ships everything you need to test CREATE, READ and UPDATE operations of your models over the default
Django admin, without writing the interaction logic yourself:

* **Auto pages** - page objects for the admin index, change-list, add-form and change-form views that resolve their
  URL automatically from a configuration feature
* **A model configuration feature** - :class:`~balderhub.django.contrib.crud.scenario_features.GeneralAdminModelConfig`,
  which describes where the admin lives and which fields are shown in the different views
* **Auto setup features** - implementations of the ``balderhub-crud`` setup features
  (:class:`~balderhub.django.contrib.crud.setup_features.AdminSingleReader`,
  :class:`~balderhub.django.contrib.crud.setup_features.AdminSingleCreator`,
  :class:`~balderhub.django.contrib.crud.setup_features.AdminSingleUpdater`,
  :class:`~balderhub.django.contrib.crud.setup_features.AdminMultipleReader`) that already know how the Django admin
  renders its forms and lists
* **Factories** - helper classes that bind the setup features to a specific data item with a single call

If you are looking for a complete end-to-end walkthrough (data items, data environment, example providers and the
final setup), take a look at the :doc:`Examples section <../examples>`. This section here focuses on the details of
the single components and how you can customize them.

The model configuration
-----------------------

Everything in this module is driven by the
:class:`~balderhub.django.contrib.crud.scenario_features.GeneralAdminModelConfig` scenario feature. For every model
(data item) you want to test, you provide one subclass and register it for the data item:

.. code-block:: python

    import balderhub.data
    import balderhub.django.contrib.crud.scenario_features
    from balderhub.url.lib.utils import Url

    from tests.lib.utils.data import BookDataItem


    @balderhub.data.register_for_data_item(BookDataItem)
    class BookAdminModelConfig(balderhub.django.contrib.crud.scenario_features.GeneralAdminModelConfig):

        @property
        def admin_root_url(self) -> Url:
            return Url("http://example.com/admin")

        @property
        def app_name(self):
            return 'bookstore'

        @property
        def model_name(self):
            return 'book'

Only ``admin_root_url``, ``app_name`` and ``model_name`` are mandatory. In addition, the config feature provides a
couple of hooks you can overwrite to describe your concrete ``ModelAdmin``:

``get_multiple_read_fields()``
    the fields that are expected as columns in the change-list view (``list_display``) - by default all fields of
    the data item

``get_single_read_fields()`` / ``get_single_create_fields()`` / ``get_single_update_fields()``
    the fields that are expected to be visible/writable in the change-form and add-form views - by default all
    fields of the data item (without ``id`` for create/update)

``get_django_field_name_for_field(field)``
    converts a data-item field name into the identifier Django uses for the corresponding form field or table
    column - overwrite this if your data item field names differ from the Django model field names

``write_date_format`` / ``write_datetime_format`` / ``read_date_format`` / ``read_datetime_format``
    the date/datetime formats used when filling or reading date fields of the admin interface

For example, if your ``ModelAdmin`` only shows some fields in ``list_display``, remove the other fields from the
multiple-read fields:

.. code-block:: python

    @balderhub.data.register_for_data_item(BookDataItem)
    class BookAdminModelConfig(balderhub.django.contrib.crud.scenario_features.GeneralAdminModelConfig):
        ...

        def get_multiple_read_fields(self) -> list[str]:
            result = super().get_multiple_read_fields()
            result.remove('summary')
            result.remove('categories')
            return result

The auto pages
--------------

The auto pages are subclasses of the general admin page objects of this package (see
:mod:`balderhub.django.lib.pages.admin`). While the general page objects require you to implement the URL schema
yourself, the auto pages read all URL information from the
:class:`~balderhub.django.contrib.crud.scenario_features.GeneralAdminModelConfig` of the same device:

* :class:`~balderhub.django.contrib.crud.pages.admin.AutoIndexPage` - the admin start page
* :class:`~balderhub.django.contrib.crud.pages.admin.AutoChangeListPage` - the change-list (table) view of the model
* :class:`~balderhub.django.contrib.crud.pages.admin.AutoAddItemFormPage` - the add form of the model
* :class:`~balderhub.django.contrib.crud.pages.admin.AutoChangeItemFormPage` - the change form of a single object

Simply assign the config feature and the pages to the same device:

.. code-block:: python

    import balder

    import balderhub.django.contrib.crud.pages.admin


    class SetupExample(balder.Setup):

        class SuperuserClient(balder.Device):
            admin_model_config = BookAdminModelConfig()

            page_index = balderhub.django.contrib.crud.pages.admin.AutoIndexPage()
            page_list = balderhub.django.contrib.crud.pages.admin.AutoChangeListPage()
            page_add = balderhub.django.contrib.crud.pages.admin.AutoAddItemFormPage()
            page_change = balderhub.django.contrib.crud.pages.admin.AutoChangeItemFormPage()

Because the pages know their model from the config, opening them does not require any arguments anymore:

.. code-block:: python

    # navigates to `http://example.com/admin/bookstore/book/add`
    self.SuperuserClient.page_add.open()
    self.SuperuserClient.page_add.wait_for_page()

The auto setup features
-----------------------

The setup features implement the abstract CRUD setup features of ``balderhub-crud`` for the Django admin. They
combine the auto pages with the model configuration and take care of everything the ready-made CRUD scenarios of
``balderhub-crud`` need:

* :class:`~balderhub.django.contrib.crud.setup_features.AdminMultipleReader` - reads all objects (with all expected
  columns) from the change-list view
* :class:`~balderhub.django.contrib.crud.setup_features.AdminSingleReader` - reads a single object from the change
  form
* :class:`~balderhub.django.contrib.crud.setup_features.AdminSingleCreator` - creates a new object over the add form
* :class:`~balderhub.django.contrib.crud.setup_features.AdminSingleUpdater` - updates an existing object over the
  change form

You can use these features without modification if your admin views use the default configuration. Every feature
must be bound to a data item. The easiest way to do that is to use the corresponding factory, which internally
creates a subclass and registers it via ``balderhub.data.register_for_data_item``:

.. code-block:: python

    import balder

    import balderhub.django.contrib.crud.setup_features.factories

    from tests.lib.utils.data import BookDataItem


    class SetupBook(balder.Setup):

        class SuperuserClient(balder.Device):
            admin_model_config = BookAdminModelConfig()
            ...

            multiple_reader = balderhub.django.contrib.crud.setup_features.factories.AutoAdminMultipleReaderFactory.get_for(BookDataItem)()
            single_reader = balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleReaderFactory.get_for(BookDataItem)()
            single_creator = balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleCreatorFactory.get_for(BookDataItem)()
            single_updater = balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleUpdaterFactory.get_for(BookDataItem)()

If you prefer explicit classes (for example because you want to overwrite some behavior), you can subclass the setup
feature yourself instead of using the factory:

.. code-block:: python

    import balderhub.data
    import balderhub.django.contrib.crud.setup_features

    from tests.lib.utils.data import BookDataItem


    @balderhub.data.register_for_data_item(BookDataItem)
    class BookAdminSingleCreator(balderhub.django.contrib.crud.setup_features.AdminSingleCreator):
        pass

With these features assigned to your setup device, the ready-made scenarios of ``balderhub-crud``
(``ScenarioSingleRead``, ``ScenarioMultipleRead``, ``ScenarioSingleCreate``, ``ScenarioSingleUpdate``) match
automatically and test the corresponding admin views.

How form fields are filled and read
-----------------------------------

Internally, the setup features build a so-called *item mapping*: for every field of the data item they look up the
corresponding form field container on the page (via
:meth:`get_form_field_container_for <balderhub.django.lib.pages.admin.ChangeFormPage>`) and select a matching
*field callback* that knows how to fill or read this widget type. The mapping between admin widgets and callbacks is
done by :func:`~balderhub.django.contrib.crud.utils.field_callbacks.get_field_filler_callback_type_for` and
:func:`~balderhub.django.contrib.crud.utils.field_callbacks.get_field_collector_callback_type_for`.

Out of the box, the following default admin widgets are supported:

.. list-table::
    :header-rows: 1
    :widths: 30 70

    * - Admin widget
      - Callbacks
    * - text/number input (``<input>``)
      - :class:`~balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminInputFillerFieldCallback` /
        :class:`~balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminInputCollectorFieldCallback`
    * - text area (``<textarea>``)
      - :class:`~balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminTextareaFillerFieldCallback` /
        :class:`~balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminTextareaCollectorFieldCallback`
    * - date field
      - :class:`~balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminDateFillerFieldCallback` /
        :class:`~balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminDateCollectorFieldCallback`
    * - foreign key (``<select>``)
      - :class:`~balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminForeignkeyFillerFieldCallback` /
        :class:`~balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminForeignkeyCollectorFieldCallback`
    * - many-to-many (filter widget)
      - :class:`~balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminM2MFillerFieldCallback` /
        :class:`~balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminM2MCollectorFieldCallback`

Values that were read from the page are always strings. The config feature converts them back into the data-item
types (``int``, ``float``, ``decimal.Decimal``, ``datetime.date``, ``datetime.datetime``, lists of them) via
:meth:`GeneralAdminModelConfig.get_collector_type_convertion_cb <balderhub.django.contrib.crud.scenario_features.GeneralAdminModelConfig.get_collector_type_convertion_cb>`,
using the ``read_date_format``/``read_datetime_format`` definitions.

Customizing for non-default admin views
---------------------------------------

If your admin views deviate from the default configuration (custom widgets, custom rendering, custom messages, ...),
subclass the relevant setup feature and overwrite the relevant methods. The most common hooks are:

``item_mapping()``
    returns the mapping between data-item fields and their field callbacks - overwrite it to use custom callbacks
    for custom widgets

``load(**kwargs)``
    opens the relevant page - overwrite it if the object cannot be reached over the default URL

``save()``
    submits the form - overwrite it if your view uses a different submit mechanism

``get_expected_error_message_for_missing_mandatory_field(...)``
    the error messages that are expected when a mandatory field is not provided - overwrite it if your project uses
    custom validation messages

For example, to support a custom widget for the ``summary`` field of a book:

.. code-block:: python

    @balderhub.data.register_for_data_item(BookDataItem)
    class BookAdminSingleCreator(balderhub.django.contrib.crud.setup_features.AdminSingleCreator):

        def item_mapping(self):
            result = super().item_mapping()
            summary_container = self.page.content.form.get_form_field_container_for(django_identifier='summary')
            result['summary'] = MyCustomSummaryFillerFieldCallback(summary_container)
            return result

The active success and error messages are extracted from the pages with
:func:`~balderhub.django.contrib.crud.utils.functions.get_success_messages_from` and
:func:`~balderhub.django.contrib.crud.utils.functions.get_error_messages_from`, which you can also reuse in your own
subclasses.

API balderhub-crud
==================

CRUD Admin Pages
----------------

.. autoclass:: balderhub.django.contrib.crud.pages.admin.AutoIndexPage
    :members:

.. autoclass:: balderhub.django.contrib.crud.pages.admin.AutoAddItemFormPage
    :members:

.. autoclass:: balderhub.django.contrib.crud.pages.admin.AutoChangeItemFormPage
    :members:

.. autoclass:: balderhub.django.contrib.crud.pages.admin.AutoChangeListPage
    :members:


CRUD Scenario Features
----------------------

.. autoclass:: balderhub.django.contrib.crud.scenario_features.GeneralAdminModelConfig
    :members:


CRUD Setup Features
-------------------

.. autoclass:: balderhub.django.contrib.crud.setup_features.AdminMultipleReader
    :members:

.. autoclass:: balderhub.django.contrib.crud.setup_features.AdminSingleCreator
    :members:

.. autoclass:: balderhub.django.contrib.crud.setup_features.AdminSingleReader
    :members:

.. autoclass:: balderhub.django.contrib.crud.setup_features.AdminSingleUpdater
    :members:

CRUD Setup Features Factories
-----------------------------

.. autoclass:: balderhub.django.contrib.crud.setup_features.factories.AutoAdminMultipleReaderFactory
    :members:

.. autoclass:: balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleCreatorFactory
    :members:

.. autoclass:: balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleReaderFactory
    :members:

.. autoclass:: balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleUpdaterFactory
    :members:

Field Callbacks
---------------

.. autofunction:: balderhub.django.contrib.crud.utils.field_callbacks.get_field_collector_callback_type_for


.. autofunction:: balderhub.django.contrib.crud.utils.field_callbacks.get_field_filler_callback_type_for


.. autoclass:: balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminDateCollectorFieldCallback
    :members:


.. autoclass:: balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminDateFillerFieldCallback
    :members:


.. autoclass:: balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminForeignkeyCollectorFieldCallback
    :members:


.. autoclass:: balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminForeignkeyFillerFieldCallback
    :members:


.. autoclass:: balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminInputCollectorFieldCallback
    :members:


.. autoclass:: balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminInputFillerFieldCallback
    :members:


.. autoclass:: balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminM2MCollectorFieldCallback
    :members:

.. autoclass:: balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminM2MFillerFieldCallback
    :members:

.. autoclass:: balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminTextareaCollectorFieldCallback
    :members:

.. autoclass:: balderhub.django.contrib.crud.utils.field_callbacks.DjangoAdminTextareaFillerFieldCallback
    :members:


CRUD Utility Functions
----------------------

.. autofunction:: balderhub.django.contrib.crud.utils.functions.convert_item_mapping_dict

.. autofunction:: balderhub.django.contrib.crud.utils.functions.extract_all_possible_schemas

.. autofunction:: balderhub.django.contrib.crud.utils.functions.get_success_messages_from

.. autofunction:: balderhub.django.contrib.crud.utils.functions.get_error_messages_from
