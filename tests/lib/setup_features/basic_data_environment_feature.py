import balderhub.data.lib.scenario_features

from balderhub.django.lib.utils import DataEnvironmentForDjangoMixin
from tests.lib.utils.data import CategoryDataItem, AuthorDataItem, BookDataItem


class BasicDataEnvironmentFeature(balderhub.data.lib.scenario_features.DataEnvironmentFeature, DataEnvironmentForDjangoMixin):

    def load_data(self):
        # --------------------------------------------------------------------------------------------------------------
        # LOAD Category
        # --------------------------------------------------------------------------------------------------------------
        self._add_data(
            self.load_from_django_fixture(
                'tests/app/bookstore/book/fixtures/categories.yaml',
                CategoryDataItem,
            )
        )

        # --------------------------------------------------------------------------------------------------------------
        # LOAD Author
        # --------------------------------------------------------------------------------------------------------------
        self._add_data(
            self.load_from_django_fixture(
                'tests/app/bookstore/book/fixtures/authors.yaml',
                AuthorDataItem,
            )
        )

        # --------------------------------------------------------------------------------------------------------------
        # LOAD Book
        # --------------------------------------------------------------------------------------------------------------

        self._add_data(
            self.load_from_django_fixture(
                'tests/app/bookstore/book/fixtures/books.yaml',
                BookDataItem,
                type_mapping=dict(price=float),
                ignore_fields=['created_at', 'updated_at'],
            )
        )