from typing import Optional
from balderhub.data.lib.utils import SingleDataItem


class CategoryDataItem(SingleDataItem):
    id: int
    name: str
    description: Optional[str]

    def get_unique_identification(self):
        return self.id
