from typing import Optional
import datetime

from balderhub.data.lib.utils import SingleDataItem


class AuthorDataItem(SingleDataItem):
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[datetime.date]
    date_of_death: Optional[datetime.date]
    biography: Optional[str]

    def get_unique_identification(self):
        return self.id
