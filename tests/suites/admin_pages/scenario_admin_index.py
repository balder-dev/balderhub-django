import balder
import balderhub.webdriver.lib.scenario_features

from tests.lib.pages import DjangoAdminIndexPage


class ScenarioAdminIndex(balder.Scenario):

    class Django(balder.Device):
        pass

    @balder.connect(Django, over_connection=balder.Connection)
    class Browser(balder.Device):
        webdriver = balderhub.webdriver.lib.scenario_features.WebdriverControlFeature()
        index_page = DjangoAdminIndexPage()

    def test_admin_index_page_is_shown(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        assert self.Browser.index_page.is_applicable()

    def test_admin_index_page_has_header(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        header = self.Browser.index_page.header
        assert header is not None

    def test_admin_index_page_header_site_name(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        header = self.Browser.index_page.header
        assert header.btn_site_name is not None
        assert "Django administration" == header.btn_site_name.text

    def test_admin_index_page_header_username(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        header = self.Browser.index_page.header
        assert header.span_username.exists()
        assert header.span_username.text == 'TESTUSER', header.span_username.text

    def test_admin_index_page_header_view_site(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        header = self.Browser.index_page.header
        assert header.btn_view_site.exists()
        assert header.btn_view_site.text == "VIEW SITE", header.btn_view_site.text

    def test_admin_index_page_header_change_password(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        header = self.Browser.index_page.header
        assert header.btn_change_password.exists()
        assert header.btn_change_password.text == "CHANGE PASSWORD", header.btn_change_password.text

    def test_admin_index_page_header_logout(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        header = self.Browser.index_page.header
        assert header.btn_logout.exists()
        assert header.btn_logout.text == "LOG OUT", header.btn_logout.text

    def test_admin_index_page_header_theme_toggle(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        header = self.Browser.index_page.header
        assert header.btn_theme_toggle.exists()

        # TODO check that theme toggeling works

    def test_admin_index_page_has_content(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        content = self.Browser.index_page.content
        assert content is not None

    def test_admin_index_page_has_app_list(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        app_list = self.Browser.index_page.content.get_app_list()
        assert len(app_list) == 2

    def test_admin_index_page_has_book_module(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        app_list = self.Browser.index_page.content.get_app_list()
        app_names = [app.a_caption.text for app in app_list]
        assert "BOOK" in app_names, app_names

    def test_admin_index_page_book_module_has_models(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        app_list = self.Browser.index_page.content.get_app_list()
        book_module = None
        for app in app_list:
            if app.a_caption.text == "BOOK":
                book_module = app
                break
        assert book_module is not None
        models = book_module.get_all_models()
        model_names = [model.a_model.text for model in models]
        assert ["Authors", "Books", "Categories"] == model_names, model_names

    def test_admin_index_page_model_row_buttons(self):
        self.Browser.index_page.open()
        self.Browser.index_page.wait_for_page()
        app_list = self.Browser.index_page.content.get_app_list()

        for app in app_list:
            assert app is not None
            models = app.get_all_models()
            for model_row in models:
                assert model_row.a_add.exists(), f"Add link missing for model {model_row.a_model.text}"
                assert model_row.a_change.exists(), f"Change link missing for model {model_row.a_model.text}"
                assert model_row.a_model.exists(), f"Model link missing"
                assert model_row.a_model.text in ['Groups', 'Users', 'Authors', 'Books', 'Categories']
