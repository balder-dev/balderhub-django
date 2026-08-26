Examples
********

This package provides ready to use page features and features for CRUD operations like CREATING, UPDATING, RETRIEVING
and DELETING with a single element or with multiple elements. This section shows some examples how you can use these
features in your own project.

All data related examples in this section use a simple bookstore application with the models ``Book``, ``Author`` and
``Category``, which are managed over the default Django admin.


Quickstart
==========

The following table provides a quick overview of the main components and their usage:

+---------------------------+------------------------------------------------------------------------------------+---------------------------------------------------+
| Component                 | Link                                                                               | Description                                       |
+===========================+====================================================================================+===================================================+
| Django Admin Page Objects | :ref:`Link <Use Django Admin Page Objects>`                                        | Ready-to-use page objects for login, index,       |
|                           |                                                                                    | change list and change form views                 |
+---------------------------+------------------------------------------------------------------------------------+---------------------------------------------------+
| CRUD Integration          | | :ref:`Link <Use the CRUD Feature Factories for testing Django Admin Operations>` | Fully Implemented CREATE, READ, UPDATE operations |
|                           | | More Details: :ref:`Link <CRUD Feature / Pages Integration>`                     | for Django admin interface                        |
+---------------------------+------------------------------------------------------------------------------------+---------------------------------------------------+
| Data Environment          | :ref:`Link <Create a Data Environment>`                                            | Load test data from Django fixtures or define     |
|                           |                                                                                    | custom data items for testing                     |
+---------------------------+------------------------------------------------------------------------------------+---------------------------------------------------+


Use Django Admin Page Objects
=============================

The package provides page objects for the most common Django admin pages:

* :class:`balderhub.django.lib.pages.admin.LoginPage` - the admin login form
* :class:`balderhub.django.lib.pages.admin.IndexPage` - the admin start page with the app/model overview
* :class:`balderhub.django.lib.pages.admin.ChangeListPage` - the list view of a model
* :class:`balderhub.django.lib.pages.admin.ChangeFormPage` - the add/change form of a single object

Since the package cannot know where your application is running, you have to subclass the page objects and provide the
URL schema of your deployment:

.. code-block:: python

    # file `lib/pages/django_admin_index_page.py`
    import os

    from balderhub.django.lib.pages.admin.index_page import IndexPage
    from balderhub.url.lib.utils import Url


    class DjangoAdminIndexPage(IndexPage):

        @property
        def applicable_on_url_schema(self) -> Url:
            return Url(f"http://example.com/admin/")

        def open(self):
            self.driver.navigate_to(self.applicable_on_url_schema)

Now you can assign the page objects to a device and use them inside your scenario or setup.

.. note::
    If you use the ``contrib.crud`` features of this package, you can define the url by using the
    :class:`balderhub.django.contrib.data.scenario_features.GeneralAdminModelConfig`.

    When using this config feature, you do not need to overwrite any implementation of the pages. Just use the page
    subclass of the contribution packages :class:`~balderhub.django.contrib.crud.pages.admin.AutoAddItemFormPage`,
    :class:`~balderhub.django.contrib.crud.pages.admin.AdminChangeItemFormPage`,
    :class:`~balderhub.django.contrib.crud.pages.admin.AdminChangeListPage`,
    :class:`~balderhub.django.contrib.crud.pages.admin.AutoIndexPage`:

    .. code-block:: python

        import os
        import balder

        import balderhub.django.contrib.data.pages
        import balderhub.django.contrib.data.scenario_features

        @balderhub.data.register_for_data_item(AuthorDataItem)
        class AuthorAdminModelConfig(balderhub.django.contrib.data.scenario_features.GeneralAdminModelConfig):
            admin_root_url = Url(f"http://example.com/admin")
            app_name = 'bookstore'
            model_name = 'author'

        class SetupExample(balder.Setup):

            class Client(balder.Device):

                author_config = AuthorAdminModelConfig()
                add_new_page = balderhub.django.contrib.crud.pages.admin.AutoAddItemFormPage()
                detail_page = balderhub.django.contrib.crud.pages.admin.AdminChangeItemFormPage()
                list_page = balderhub.django.contrib.crud.pages.admin.AdminChangeListPage()
                ...


The following example shows a fixture to log in into the django admin by using the
:class:`~balderhub.django.lib.pages.admin.LoginPage`:

.. code-block:: python

    import os
    import balder

    from tests.lib.pages import DjangoAdminLoginPage, DjangoAdminIndexPage


    class SetupExample(balder.Setup):

        class SuperuserClient(balder.Device):
            login_page = balderhub.django.lib.pages.admin.LoginPage()
            index_page = balderhub.django.lib.pages.admin.IndexPage()
            ...

        @balder.fixture('variation')
        def make_sure_to_be_logged_in(self):
            self.SuperuserClient.login_page.open()
            if self.SuperuserClient.login_page.is_applicable():
                username = ...
                password = ...

                self.SuperuserClient.login_page.input_username.type_text(username, clean_before=True)
                self.SuperuserClient.login_page.input_password.type_text(password, clean_before=True)
                self.SuperuserClient.login_page.btn_login.click()
                self.SuperuserClient.index_page.wait_for_page()

Work with the change-list page
------------------------------

The change-list page object gives you comfortable access to the header, the breadcrumbs, the search bar, the filter
sidebar and of course the result table. The following scenario shows some typical interactions:

.. code-block:: python

    import balder
    import balderhub.webdriver.lib.scenario_features

    from tests.lib.pages import DjangoAdminChangeListPage


    class ScenarioAdminChangeList(balder.Scenario):

        class Django(balder.Device):
            pass

        @balder.connect(Django, over_connection=balder.Connection)
        class Browser(balder.Device):
            webdriver = balderhub.webdriver.lib.scenario_features.WebdriverControlFeature()
            change_list_page = DjangoAdminChangeListPage()

        def test_list_table(self):
            # open the change list of the model `book` in the app `book`
            self.Browser.change_list_page.open(app='book', model='book')
            self.Browser.change_list_page.wait_for_page()

            table = self.Browser.change_list_page.content.result_table

            # access the column headers
            header_title = table.get_table_column_header_for('title')
            assert header_title.text == "TITLE"

            # access rows and single cells
            rows = table.get_rows()
            first_row = table.get_row_at(0)
            cell_title = first_row.get_cell_for('title')
            assert cell_title.text == "A Christmas Carol"

            # or address a cell directly by column name and row index
            cell_author = table.get_table_cell_for('author', 0)
            assert cell_author.text == "Dickens, Charles"

        def test_list_filters(self):
            self.Browser.change_list_page.open(app='book', model='book')
            self.Browser.change_list_page.wait_for_page()

            filter_sidebar = self.Browser.change_list_page.content.filter_sidebar
            filters = filter_sidebar.get_filters()
            author_filter = filters[1]
            assert author_filter.h3_title.text == "By author"
            choices = author_filter.get_choices()

Other useful elements of the change-list page are ``self.Browser.change_list_page.header`` (site name, username,
logout button, theme toggle, ...), ``self.Browser.change_list_page.breadcrumbs``,
``self.Browser.change_list_page.btn_add`` (the *ADD* button) and ``self.Browser.change_list_page.content``
with ``input_search``, ``btn_search``, ``select_action``, ``btn_action_go`` and ``span_result_count``.

Work with the change-form page
------------------------------

The change-form page object knows the fieldsets and form fields of the Django admin form. The provided field
containers support the standard admin widgets (text inputs, text areas, dates, foreign keys and many-to-many
relations):

.. code-block:: python

    def test_change_book_title(self):
        # open the change form of the book with the primary key 1
        self.Browser.change_form_page.open(app='book', model='book', item_id=1)
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        field_title = form.get_form_field_container_for(django_identifier='title')
        field_title.set_value('A new title')

        self.Browser.change_form_page.content.submit_row.btn_save.click()


Create a Data Environment
=========================

This is a short overview how you can create a data environment. Please refer to the
`balderhub-data documentation <https://hub.balder.dev/projects/data>` for more details.

A data environment describes the data your test expects on the server side. It works with so called *data items*,
which are simple typed classes that describe one record of your model. Similar to the existing Django models you
can create the same data structure by defining subclass of ``balderhub.data.lib.utils.SingleDataItem``.

.. note::
    Note that the data structure you define here in the test does not have to be exactly the same as in the Django
    model. Always try to tailor it to your testing scope

.. code-block:: python

    # file `lib/utils/data/book_data_item.py`
    from typing import Optional
    import datetime

    from balderhub.data.lib.utils import SingleDataItem

    from .author_data_item import AuthorDataItem
    from .category_data_item import CategoryDataItem


    class BookDataItem(SingleDataItem):
        id: int
        title: str
        author: AuthorDataItem
        categories: list[CategoryDataItem]
        isbn: str
        summary: Optional[str]
        publication_date: Optional[datetime.date]
        price: Optional[float]
        pages: Optional[int]

        def get_unique_identification(self):
            return self.id

As you can see, data items can reference each other. The ``author`` field holds another data item and the
``categories`` field holds a list of data items - exactly like the ``ForeignKey`` and ``ManyToManyField`` of the
Django model.

The data environment itself is a feature that derives from
:class:`balderhub.data.lib.scenario_features.DataEnvironmentFeature`. You have to implement the ``load_data()`` method,
in which you add all data items that exist on the server:

.. code-block:: python

    # file `lib/setup_features/basic_data_environment_feature.py`
    import balderhub.data.lib.scenario_features
    import balderhub.django.lib.utils

    from tests.lib.utils.data import AuthorDataItem


    class BasicDataEnvironmentFeature(balderhub.django.lib.utils.DataEnvironmentForDjangoMixin):

        def load_data(self):
            self._add_data([
                AuthorDataItem(id=1, first_name='Jane', last_name='Austen'),
                AuthorDataItem(id=2, first_name='Charles', last_name='Dickens'),
                ...
            ])

Of course, adding every single item by hand does not scale. If your Django project already provides django fixtures, you
can load them directly - see the next section.

Use the Django Mixin
--------------------

If you would like to load test data from django fixtures you can also use the
:class:`balderhub.django.lib.utils.DataEnvironmentForDjangoMixin`:

Assume your Django app ships fixtures like this one:

.. code-block:: yaml

    # file `app/bookstore/book/fixtures/books.yaml`
    - model: book.book
      pk: 1
      fields:
        title: Pride and Prejudice
        author: 1
        isbn: '9780141439518'
        summary: A romantic novel following Elizabeth Bennet as she navigates issues of manners, morality, and marriage.
        publication_date: 1813-01-28
        price: '12.99'
        pages: 432
        categories: [1, 2, 3]
        created_at: '1970-01-01 00:00:00+00:00'
        updated_at: '1970-01-01 00:00:00+00:00'

Simply add the mixin to your data environment feature and use its
:meth:`load_from_django_fixture <balderhub.django.lib.utils.DataEnvironmentForDjangoMixin.load_from_django_fixture>`
method inside ``load_data()``:

.. code-block:: python

    # file `lib/setup_features/basic_data_environment_feature.py`
    import balderhub.data.lib.scenario_features

    from balderhub.django.lib.utils import DataEnvironmentForDjangoMixin
    from tests.lib.utils.data import CategoryDataItem, AuthorDataItem, BookDataItem


    class BasicDataEnvironmentFeature(
            balderhub.data.lib.scenario_features.DataEnvironmentFeature,
            DataEnvironmentForDjangoMixin,
    ):

        def load_data(self):
            # LOAD Category
            self._add_data(
                self.load_from_django_fixture(
                    'app/bookstore/book/fixtures/categories.yaml',
                    CategoryDataItem,
                )
            )

            # LOAD Author
            self._add_data(
                self.load_from_django_fixture(
                    'app/bookstore/book/fixtures/authors.yaml',
                    AuthorDataItem,
                )
            )

            # LOAD Book
            self._add_data(
                self.load_from_django_fixture(
                    'app/bookstore/book/fixtures/books.yaml',
                    BookDataItem,
                    type_mapping=dict(price=float),
                    ignore_fields=['created_at', 'updated_at'],
                )
            )

Some things worth knowing about ``load_from_django_fixture()``:

* **Relations are resolved automatically**: If a data item field is another ``SingleDataItem`` (or a list of them),
  the mixin resolves the primary keys from the fixture to the already loaded data items. That is why the categories
  and authors are loaded *before* the books in the example above.
* **Type conversion**: Django fixtures often store values as strings (like the ``price`` in the example). With the
  ``type_mapping`` argument you can provide a converter callable per field.
* **Ignoring fields**: Fields that exist in the fixture but not in your data item (like ``created_at`` and
  ``updated_at``) can be skipped with the ``ignore_fields`` argument.
* **Primary key field**: By default the primary key of the fixture is mapped to the field ``id`` of your data item.
  If one of your data items uses a different primary key field name, overwrite the class attribute ``PK_FIELDS``:

  .. code-block:: python

      class MyDataEnvironment(
              balderhub.data.lib.scenario_features.DataEnvironmentFeature,
              DataEnvironmentForDjangoMixin,
      ):
          PK_FIELDS = {
              BookDataItem: 'id',
              IsbnEntryDataItem: 'isbn',
          }

Use the CRUD Feature Factories for testing Django Admin Operations
==================================================================

The real power of this package is its integration with ``balderhub-crud``. Instead of writing your own tests for
CREATE, READ and UPDATE operations, you can use the ready-made scenarios of ``balderhub-crud`` and only provide the
configuration for your models. The setup features :class:`balderhub.django.contrib.crud.setup_features.AdminSingleReader`,
:class:`balderhub.django.contrib.crud.setup_features.AdminSingleCreator`,
:class:`balderhub.django.contrib.crud.setup_features.AdminSingleUpdater` and
:class:`balderhub.django.contrib.crud.setup_features.AdminMultipleReader` already know how the Django admin renders
its forms and lists, so they work out of the box for default admin configurations.

Provide a model configuration
-----------------------------

For every model you want to test, you need a
:class:`balderhub.django.contrib.crud.scenario_features.GeneralAdminModelConfig`. It describes where the admin lives
and which fields are shown in the different admin views. Register it for your data item with
``@balderhub.data.register_for_data_item``:

.. code-block:: python

    import os

    import balderhub.data
    import balderhub.django.contrib.crud.scenario_features
    from balderhub.url.lib.utils import Url

    from tests.lib.utils.data import BookDataItem


    @balderhub.data.register_for_data_item(BookDataItem)
    class GeneralAdminModelConfig(balderhub.django.contrib.crud.scenario_features.GeneralAdminModelConfig):
        admin_root_url = Url(f"http://example.com/admin")
        app_name = 'bookstore'
        model_name = 'book'

        def get_multiple_read_fields(self) -> list[str]:
            # by default all data item fields are expected in the change list -
            # remove the fields that are not part of `list_display` of your ModelAdmin
            result = super().get_multiple_read_fields()
            result.remove('summary')
            result.remove('categories')
            return result

Provide example data
--------------------

The CRUD scenarios need to know which data they should use for creating and updating objects. For this, implement the
example providers of ``balderhub-crud`` and register them for your data item as well:

.. code-block:: python

    import balder
    import balderhub.data
    import balderhub.crud.lib.scenario_features
    from balderhub.data.lib.utils import NOT_DEFINABLE

    from tests.lib.setup_features.basic_data_environment_feature import BasicDataEnvironmentFeature
    from tests.lib.utils.data import BookDataItem, CategoryDataItem, AuthorDataItem


    @balderhub.data.register_for_data_item(BookDataItem)
    class CreateExampleProvider(balderhub.crud.lib.scenario_features.SingleCreateExampleProvider):

        class Server(balder.VDevice):
            env = BasicDataEnvironmentFeature()

        def get_valid_examples(self):
            category = self.Server.env.get(CategoryDataItem, 1)
            author = self.Server.env.get(AuthorDataItem, 1)
            return [
                self.NamedExample(
                    name='New Book',
                    data_item=BookDataItem(
                        id=NOT_DEFINABLE,  # the id will be assigned by the server
                        title='New very nice Book',
                        author=author,
                        categories=[category],
                        isbn='1234567890',
                        summary="This is a very nice book with an interesting content",
                        publication_date=None,
                        price=1.99,
                        pages=123,
                    )
                )
            ]

        def get_invalid_examples(self):
            return []

Assemble the setup
------------------

Now everything comes together in a setup class. Use the factories to create data-item bound versions of the setup
features - calling ``get_for(<YourDataItem>)`` returns a feature class that is registered for exactly this data item:

.. code-block:: python

    import balder

    import balderhub.data.lib.setup_features.factories
    import balderhub.crud.lib.setup_features.factories
    import balderhub.django.contrib.crud.pages
    import balderhub.django.contrib.crud.setup_features

    from tests.lib.setup_features.basic_data_environment_feature import BasicDataEnvironmentFeature
    from tests.lib.setup_features.data import book
    from tests.lib.setup_features.selenium_feature import SeleniumFeature
    from tests.lib.pages import DjangoAdminIndexPage, DjangoAdminLoginPage
    from tests.lib.utils.data import BookDataItem


    class SetupBook(balder.Setup):

        class Server(balder.Device):
            env = BasicDataEnvironmentFeature()
            initial_data = balderhub.data.lib.setup_features.factories.AutoInitialDataConfigFactory.get_for(BookDataItem)()

        @balder.connect(Server, over_connection=balder.Connection)
        class SuperuserClient(balder.Device):

            selenium = SeleniumFeature()

            # the model configuration and the example providers from above
            admin_model_config = book.GeneralAdminModelConfig()
            example_create = book.CreateExampleProvider(Server='Server')
            example_update = book.UpdateFieldExampleProvider()
            example_single_read = balderhub.crud.lib.setup_features.factories.AutoSingleReadExampleFactory.get_for(BookDataItem)()

            # the page objects
            login_page = DjangoAdminLoginPage()
            index_page = DjangoAdminIndexPage()
            page_add = balderhub.django.contrib.crud.pages.AdminAddItemFormPage()
            page_update = balderhub.django.contrib.crud.pages.AdminChangeItemFormPage()
            page_list = balderhub.django.contrib.crud.pages.AdminChangeListPage()

            # the CRUD setup features, created by the factories of this package
            multiple_reader = balderhub.django.contrib.crud.setup_features.factories.AutoAdminMultipleReaderFactory.get_for(BookDataItem)()
            single_reader = balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleReaderFactory.get_for(BookDataItem)()
            single_creator = balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleCreatorFactory.get_for(BookDataItem)()
            single_updater = balderhub.django.contrib.crud.setup_features.factories.AutoAdminSingleUpdaterFactory.get_for(BookDataItem)()

            multiple_data_with_auth = balderhub.data.lib.setup_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(BookDataItem)(Master="Server")

Activate the ready-made scenarios
---------------------------------

Finally, activate the CRUD scenarios of ``balderhub-crud`` by simply importing them into your test environment:

.. code-block:: python

    from balderhub.crud.scenarios import (
        ScenarioSingleRead,
        ScenarioMultipleRead,
        ScenarioSingleUpdate,
        ScenarioSingleCreate,
    )

That's all. When you now run Balder, the imported scenarios will match with your setup and automatically test that:

* a single object can be read over the admin change form and shows the expected data (``ScenarioSingleRead``)
* the admin change list shows all expected objects with the expected values (``ScenarioMultipleRead``)
* new objects can be created over the admin add form (``ScenarioSingleCreate``)
* existing objects can be updated over the admin change form (``ScenarioSingleUpdate``)
* optional fields are really optional, vice versa for mandatory fields
* specific defined invalid examples show the correct and expected error messages

If your admin views deviate from the default configuration (custom widgets, custom field rendering, ...), you can
subclass the setup features (for example :class:`balderhub.django.contrib.crud.setup_features.AdminSingleReader`)
instead of using the factories and overwrite the relevant methods like ``item_mapping()`` or ``load()``.
