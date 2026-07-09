from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature
from balderhub.url.lib.utils import Url


class GeneralAdminModelConfig(AbstractDataItemRelatedFeature):
    """
    This class provides configuration for administrative models wherein it defines
    important settings, including root URL, application name in django admin pages.
    """
    @property
    def admin_root_url(self) -> Url:
        """the root URL for administrative actions related to the model."""
        raise NotImplementedError

    @property
    def app_name(self):
        """the name of the application associated with the model."""
        raise NotImplementedError

    @property
    def model_name(self):
        """the name of the model."""
        raise NotImplementedError
