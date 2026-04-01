import balderhub.data
from balderhub.data.lib.utils.auto_feature_factory import AutoFeatureFactory
from balderhub.data.lib.utils.single_data_item import SingleDataItem

from ..admin_single_reader import AdminSingleReader


class AutoAdminSingleReaderFactory(AutoFeatureFactory):
    """
    Factory for creating data-item bounded setup-based config-feature :class:`AdminSingleReader`
    """

    @classmethod
    def _define_class(cls, data_item_cls: type[SingleDataItem], **kwargs) -> type[AdminSingleReader]:

        @balderhub.data.register_for_data_item(data_item_cls)
        class AutoAdminSingleReader(AdminSingleReader):
            """inner factory-created feature class"""

        return AutoAdminSingleReader
