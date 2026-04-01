import balderhub.data
from balderhub.data.lib.utils.auto_feature_factory import AutoFeatureFactory
from balderhub.data.lib.utils.single_data_item import SingleDataItem

from ..admin_single_creator import AdminSingleCreator


class AutoAdminSingleCreatorFactory(AutoFeatureFactory):
    """
    Factory for creating data-item bounded setup-based config-feature :class:`AdminSingleCreator`
    """

    @classmethod
    def _define_class(cls, data_item_cls: type[SingleDataItem], **kwargs) -> type[AdminSingleCreator]:

        @balderhub.data.register_for_data_item(data_item_cls)
        class AutoAdminSingleCreator(AdminSingleCreator):
            """inner factory-created feature class"""

        return AutoAdminSingleCreator
