import balder
import balderhub.webdriver.lib.scenario_features

from balderhub.django.lib.utils.gui.admin.change_form_fields import BaseChangeFormField, TextareaChangeFormField
from tests.lib.pages import DjangoAdminChangeFormPage
from balderhub.django.lib.utils.gui.admin.change_form_fields import (
    InputChangeFormField,
    ForeignKeyChangeFormField,
    M2MChangeFormField,
    DateChangeFormField
)


class ScenarioAdminChangeForm(balder.Scenario):

    class Django(balder.Device):
        pass

    @balder.connect(Django, over_connection=balder.Connection)
    class Browser(balder.Device):
        webdriver = balderhub.webdriver.lib.scenario_features.WebdriverControlFeature()
        change_form_page = DjangoAdminChangeFormPage()

    def test_change_form_page_is_shown(self):
        # Using a book with id 1 from the fixture data
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        assert self.Browser.change_form_page.is_applicable()

    def test_change_form_content_basic(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        
        # 'Pride and Prejudice' is the title of book with id 1 in the fixtures
        assert "Change book" in self.Browser.change_form_page.content.h1_title.text
        # Django admin usually shows the object's __str__ as a caption/h2
        assert self.Browser.change_form_page.content.h2_caption.text == "Pride and Prejudice"

    # --- Header selectors ---

    def test_change_form_header_site_name(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        header = self.Browser.change_form_page.header
        assert header.btn_site_name.exists()
        assert header.btn_site_name.text == "Django administration"

    def test_change_form_header_username(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        header = self.Browser.change_form_page.header
        assert header.span_username.exists()
        assert header.span_username.text == 'TESTUSER', header.span_username.text

    def test_change_form_header_view_site(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        header = self.Browser.change_form_page.header
        assert header.btn_view_site.exists()
        assert header.btn_view_site.text == "VIEW SITE", header.btn_view_site.text

    def test_change_form_header_change_password(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        header = self.Browser.change_form_page.header
        assert header.btn_change_password.exists()

    def test_change_form_header_logout(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        header = self.Browser.change_form_page.header
        assert header.btn_logout.exists()

    def test_change_form_header_theme_toggle(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        header = self.Browser.change_form_page.header
        assert header.btn_theme_toggle.exists()

        # TODO check if theme was toggled!

    # --- Breadcrumbs ---

    def test_change_form_breadcrumbs_exist(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        breadcrumbs = self.Browser.change_form_page.breadcrumbs
        assert breadcrumbs.exists()

    def test_change_form_breadcrumbs_links(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        breadcrumbs = self.Browser.change_form_page.breadcrumbs
        links = breadcrumbs.get_links()
        # Expect: Home > Book > Books > Pride and Prejudice (last one has no link)
        assert len(links) == 3, f"Expected 3 breadcrumb links, got {len(links)}"
        assert links[0].text == "Home", links[0].text
        assert links[1].text == "Book", links[1].text
        assert links[2].text == "Books", links[2].text

        breadcrumb_items = breadcrumbs.get_items_as_texts()
        assert breadcrumb_items == ["Home", "Book", "Books", "Pride and Prejudice"], breadcrumb_items

    # --- Form structure ---

    def test_change_form_field_types(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        
        form = self.Browser.change_form_page.content.form
        assert form.exists()

        fieldsets = form.get_all_fieldsets()
        assert len(fieldsets) == 1

        all_rows = fieldsets[0].get_all_rows()
        assert len(all_rows) == 6, all_rows

        # Check if submit row exists
        assert form.submit_row.exists()

        def val_row(row_field_containers, expected_labels_and_type: dict[str, type[BaseChangeFormField]]):
            assert len(row_field_containers) == len(expected_labels_and_type), \
                f"unexpected length of {len(row_field_containers)}, expected {expected_labels_and_type}"
            remaining_labels_and_type = expected_labels_and_type.copy()

            for field in row_field_containers:
                field_label_text = field.label.text.strip(': ')
                expected_field_type = expected_labels_and_type[field_label_text]

                if field_label_text not in expected_labels_and_type.keys():
                    raise ValueError(f"field `{field_label_text}` is not in {expected_labels_and_type}")

                if not isinstance(field, expected_field_type):
                    raise TypeError(
                        f"field with label `{field_label_text}` is not of type {expected_field_type} "
                        f"- is type {type(field)}"
                    )

                del remaining_labels_and_type[field_label_text]

            assert len(remaining_labels_and_type) == 0, f'did not found fields {remaining_labels_and_type} in row'

        # Based on BookAdmin fields definition:
        # fields = (
        #     ('title', ),
        #     ('author',),
        #     ('categories',),
        #     ('price', 'publication_date', 'isbn'),
        #     ('pages', )
        #     ('summary', )
        # )
        val_row(all_rows[0].get_all_field_container(), {'Title': InputChangeFormField})
        val_row(all_rows[1].get_all_field_container(), {'Author': ForeignKeyChangeFormField})
        val_row(all_rows[2].get_all_field_container(), {'Categories': M2MChangeFormField})
        val_row(all_rows[3].get_all_field_container(), {
            'Price': InputChangeFormField,
            'Publication date': DateChangeFormField,
            'ISBN': InputChangeFormField,
        })
        val_row(all_rows[4].get_all_field_container(), {'Pages': InputChangeFormField})
        val_row(all_rows[5].get_all_field_container(), {'Summary': TextareaChangeFormField})
    # --- Submit row buttons ---

    def test_change_form_submit_row_btn_save(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        submit_row = self.Browser.change_form_page.content.form.submit_row
        assert submit_row.btn_save.exists()

    def test_change_form_submit_row_btn_save_and_continue(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        submit_row = self.Browser.change_form_page.content.form.submit_row
        assert submit_row.btn_save_and_continue.exists()

    def test_change_form_submit_row_btn_save_and_add_another(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        submit_row = self.Browser.change_form_page.content.form.submit_row
        assert submit_row.btn_save_and_add_another.exists()

    def test_change_form_submit_row_delete_link(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        submit_row = self.Browser.change_form_page.content.form.submit_row
        assert submit_row.a_delete.exists()


    # --- ForeignKey field selectors ---

    def test_change_form_fk_field_validate_buttons(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        all_rows = form.get_all_fieldsets()[0].get_all_rows()
        author_field = all_rows[1].get_all_field_container()[0]
        assert isinstance(author_field, ForeignKeyChangeFormField)
        assert author_field.field.exists()
        assert author_field.btn_add.exists()
        assert author_field.btn_change_related.exists()
        assert author_field.btn_delete.exists()
        assert author_field.btn_view_related.exists()


    # --- M2M field / widget selectors ---

    def test_change_form_m2m_field_widget(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        all_rows = form.get_all_fieldsets()[0].get_all_rows()
        categories_field = all_rows[2].get_all_field_container()[0]
        assert isinstance(categories_field, M2MChangeFormField)
        assert categories_field.field.exists()
        assert isinstance(categories_field, M2MChangeFormField)
        assert categories_field.btn_add.exists()

        widget = categories_field.field

        assert widget.div_available_selector.exists()
        assert widget.div_available_selector.input_selector_filter.exists()
        assert widget.div_available_selector.select.exists()
        assert widget.div_chosen_selector.exists()
        assert widget.div_chosen_selector.input_selector_filter.exists()
        assert widget.div_chosen_selector.select.exists()
        assert widget.btn_arrow_add.exists()
        assert widget.btn_arrow_remove.exists()
        assert widget.btn_choose_all.exists()
        assert widget.btn_choose_none.exists()

    # --- Date field selectors ---

    def test_change_form_date_field_input(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        all_rows = form.get_all_fieldsets()[0].get_all_rows()
        # publication_date is in row 3 (index 3), second field
        row3_fields = all_rows[3].get_all_field_container()
        date_field = None
        for f in row3_fields:
            if isinstance(f, DateChangeFormField):
                date_field = f
                break
        assert date_field is not None, "Date field not found in row 3"

        assert date_field.field.exists()
        assert date_field.btn_shortcut_today.exists()
        assert date_field.btn_open_calendar.exists()

    # --- get_all_form_field_containers ---

    def test_get_all_form_field_containers_returns_all_fields(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        all_fields = form.get_all_form_field_containers()
        # Book has 8 fields: title, author, categories, price, publication_date, isbn, pages, summary
        assert len(all_fields) == 8, f"Expected 8 field containers, got {len(all_fields)}"

        expected_types = [
            InputChangeFormField,        # title
            ForeignKeyChangeFormField,    # author
            M2MChangeFormField,           # categories
            InputChangeFormField,         # price
            DateChangeFormField,          # publication_date
            InputChangeFormField,         # isbn
            InputChangeFormField,         # pages
            TextareaChangeFormField,      # summary
        ]
        for i, (field, expected_type) in enumerate(zip(all_fields, expected_types)):
            assert isinstance(field, expected_type), \
                f"Field at index {i} is {type(field).__name__}, expected {expected_type.__name__}"

    # --- get_form_field_container_for ---

    def test_get_form_field_container_for_title(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        field = form.get_form_field_container_for('title')
        assert isinstance(field, InputChangeFormField)
        assert field.label.text.strip(': ') == 'Title'

    def test_get_form_field_container_for_author(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        field = form.get_form_field_container_for('author')
        assert isinstance(field, ForeignKeyChangeFormField)
        assert field.label.text.strip(': ') == 'Author'

    def test_get_form_field_container_for_categories(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        field = form.get_form_field_container_for('categories')
        assert isinstance(field, M2MChangeFormField)
        assert field.label.text.strip(': ') == 'Categories'

    def test_get_form_field_container_for_publication_date(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        field = form.get_form_field_container_for('publication_date')
        assert isinstance(field, DateChangeFormField)
        assert field.label.text.strip(': ') == 'Publication date'

    def test_get_form_field_container_for_price(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        field = form.get_form_field_container_for('price')
        assert isinstance(field, InputChangeFormField)
        assert field.label.text.strip(': ') == 'Price'

    def test_get_form_field_container_for_isbn(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        field = form.get_form_field_container_for('isbn')
        assert isinstance(field, InputChangeFormField)
        assert field.label.text.strip(': ') == 'ISBN'

    def test_get_form_field_container_for_pages(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        field = form.get_form_field_container_for('pages')
        assert isinstance(field, InputChangeFormField)
        assert field.label.text.strip(': ') == 'Pages'

    def test_get_form_field_container_for_nonexistent_raises(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()

        form = self.Browser.change_form_page.content.form
        try:
            form.get_form_field_container_for('nonexistent_field')
            assert False, "Expected ValueError was not raised"
        except ValueError as exc:
            assert exc.args[0] == "no form field container found for django identifier `nonexistent_field`", exc.args[0]

    # --- Object tools ---

    def test_change_form_object_tools(self):
        self.Browser.change_form_page.open(app='book', model='book', object_id='1')
        self.Browser.change_form_page.wait_for_page()
        assert self.Browser.change_form_page.content.object_tools.exists()
