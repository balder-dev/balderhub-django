from typing import Optional
import datetime

from balderhub.data.lib.utils import SingleDataItem
from .author_data_item import AuthorDataItem
from .category_data_item import CategoryDataItem


class BookDataItem(SingleDataItem):
    id: int
    title: str
    author: AuthorDataItem
    categories: Optional[list[CategoryDataItem]] # TODO
    isbn: str
    summary: Optional[str]
    publication_date: Optional[datetime.date]
    price: Optional[float]
    pages: Optional[int]
    #created_at: datetime.datetime
    #updated_at: datetime.datetime

    def get_unique_identification(self):
        return self.id
