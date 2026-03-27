import os

from selenium.webdriver import FirefoxOptions
from balderhub.selenium.lib.setup_features import SeleniumRemoteWebdriverFeature


class SeleniumFeature(SeleniumRemoteWebdriverFeature):

    @property
    def command_executor(self) -> str:
        hostname = os.getenv('SELENIUM_HOSTNAME', 'localhost')
        return f"http://{hostname}:4444"

    @property
    def selenium_options(self) -> FirefoxOptions:
        options = FirefoxOptions()
        return options