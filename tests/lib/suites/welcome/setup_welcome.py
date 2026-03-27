import balder
from tests.lib.setup_features.selenium_feature import SeleniumFeature
from tests.lib.pages import DjangoWelcomePage


class SetupWelcome(balder.Setup):

    class Server(balder.Device):
        pass

    @balder.connect(Server, over_connection=balder.Connection)
    class Browser(balder.Device):
        selenium = SeleniumFeature()
        welcome_page = DjangoWelcomePage()


    @balder.fixture('testcase')
    def connect_selenium(self):
        self.Browser.selenium.create()
        yield
        self.Browser.selenium.quit()
