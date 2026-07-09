import balder
import balderhub.webdriver.lib.scenario_features
from tests.lib.pages import DjangoWelcomePage


class ScenarioWelcome(balder.Scenario):

    class Django(balder.Device):
        pass

    @balder.connect(Django, over_connection=balder.Connection)
    class Browser(balder.Device):
        webdriver = balderhub.webdriver.lib.scenario_features.WebdriverControlFeature()
        welcome_page = DjangoWelcomePage()

    def test_welcome_page_is_shown(self):
        self.Browser.welcome_page.open()
        self.Browser.welcome_page.wait_for_page()
        assert self.Browser.welcome_page.is_applicable()
        assert "The install worked successfully! Congratulations!" == self.Browser.welcome_page.h1_title.text, self.Browser.welcome_page.h1_title.text
