from typing import Optional
from balderhub.data.lib.utils import SingleDataItem

from tests.lib.utils.data import BookDataItem


class BookReviewDataItem(SingleDataItem):
    id: int
    for_book: BookDataItem
    stars: int
    text: Optional[str]
    #created_at: datetime.datetime
    #updated_at: datetime.datetime

    def get_unique_identification(self):
        return self.id
