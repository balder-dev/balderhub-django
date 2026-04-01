import balder
import balderhub.webdriver.lib.scenario_features
from balderhub.html.lib.utils import Selector

from tests.lib.pages import DjangoAdminChangeListPage


class ScenarioAdminChangeList(balder.Scenario):

    class Django(balder.Device):
        pass

    @balder.connect(Django, over_connection=balder.Connection)
    class Browser(balder.Device):
        webdriver = balderhub.webdriver.lib.scenario_features.WebdriverControlFeature()
        change_list_page = DjangoAdminChangeListPage()

    def test_list_page_is_shown(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        assert self.Browser.change_list_page.is_applicable()

    # --- Header selectors ---

    def test_list_header_site_name(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        header = self.Browser.change_list_page.header
        assert header.btn_site_name.exists()
        assert header.btn_site_name.text == "Django administration"

    def test_list_header_username(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        header = self.Browser.change_list_page.header
        assert header.span_username.exists()
        assert header.span_username.text == 'TESTUSER'

    def test_list_header_view_site(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        header = self.Browser.change_list_page.header
        assert header.btn_view_site.exists()
        assert header.btn_view_site.text == "VIEW SITE", header.btn_view_site.text

    def test_list_header_change_password(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        header = self.Browser.change_list_page.header
        assert header.btn_change_password.exists()

    def test_list_header_logout(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        header = self.Browser.change_list_page.header
        assert header.btn_logout.exists()

    def test_list_header_theme_toggle(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        header = self.Browser.change_list_page.header
        assert header.btn_theme_toggle.exists()

        # TODO validate if theme changed

    # --- Breadcrumbs ---

    def test_list_breadcrumbs_exist(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        breadcrumbs = self.Browser.change_list_page.breadcrumbs
        assert breadcrumbs.exists()

    def test_list_breadcrumbs_links(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        breadcrumbs = self.Browser.change_list_page.breadcrumbs
        links = breadcrumbs.get_links()

        # Expect: Home > Book > Books (last one has no link)
        assert len(links) == 2, f"Expected 2 breadcrumb links, got {len(links)}"
        assert links[0].text == "Home", links[0].text
        assert links[1].text == "Book", links[1].text

        breadcrumb_items = breadcrumbs.get_items_as_texts()
        assert breadcrumb_items == ["Home", "Book", "Books"], breadcrumb_items

    # --- Search bar ---

    def test_list_search_bar_exists(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        assert self.Browser.change_list_page.content.input_search.exists()
        assert self.Browser.change_list_page.content.btn_search.exists()


    # --- Action bar ---

    def test_list_action_select_exists(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        assert self.Browser.change_list_page.content.select_action.exists()
        assert self.Browser.change_list_page.content.btn_action_go.exists()

    # --- Add button ---

    def test_list_add_button_exists(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        assert self.Browser.change_list_page.btn_add.exists()

    # --- Result count ---

    def test_list_result_count(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        result_count = self.Browser.change_list_page.content.span_result_count
        assert result_count.exists()
        assert "99 books" == result_count.text, result_count.text

    # --- Result table ---

    def test_list_result_table_exists(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        table = self.Browser.change_list_page.content.result_table
        assert table.exists()

    def test_list_table_headers(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        table = self.Browser.change_list_page.content.result_table

        # Check specific headers using the helper method
        header_title = table.get_table_column_header_for('title')
        assert "TITLE" == header_title.text, header_title.text

        header_author = table.get_table_column_header_for('author')
        assert "AUTHOR" == header_author.text, header_author.text

        header_isbn = table.get_table_column_header_for('isbn')
        assert "ISBN" == header_isbn.text, header_isbn.text

        header_pub_date = table.get_table_column_header_for('publication_date')
        assert "PUBLICATION DATE" == header_pub_date.text, header_pub_date.text

        header_price = table.get_table_column_header_for('price')
        assert "PRICE" == header_price.text, header_price.text

    def test_list_table_all_column_headers(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        table = self.Browser.change_list_page.content.result_table

        # BookAdmin.list_display = ['title', 'author', 'isbn', 'publication_date', 'price']
        # Django also adds a checkbox column header
        headers = table.get_header_cells()
        header_texts = [h.text for h in headers]
        assert header_texts == ["", "ID", "TITLE", "AUTHOR", "ISBN", "PUBLICATION DATE", "PRICE"], header_texts
        assert headers[0].bridge.find_bridge(Selector.by_tag('input')).exists(), 'did not find global checkbox'

    def test_list_table_rows_exist(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        table = self.Browser.change_list_page.content.result_table
        rows = table.get_rows()
        assert len(rows) == 99, f"Expected exactly 99 rows in the result table, found {len(rows)}"

    def test_list_table_row_has_cells(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        table = self.Browser.change_list_page.content.result_table
        row = table.get_row_at(0)
        cells = row.get_cells()
        # list_display has 6 fields + action checkbox column
        assert len(cells) == 6, f"Expected to have 6 cells (with action checkbox), got {len(cells)}"
        assert row.checkbox.exists()
        assert row.a_link.exists()
        assert 1 <= int(row.a_link.text) <= 100, row.a_link.text

    def test_list_table_row_get_cell_for(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        table = self.Browser.change_list_page.content.result_table
        row = table.get_row_at(0)

        cell_title = row.get_cell_for('title')
        assert cell_title.exists()
        assert cell_title.text == "A Christmas Carol", cell_title.text

        cell_author = row.get_cell_for('author')
        assert cell_author.exists()
        assert cell_author.text == "Dickens, Charles", cell_author.text

        cell_isbn = row.get_cell_for('isbn')
        assert cell_isbn.exists()
        assert cell_isbn.text == "9780141389479", cell_isbn.text

        cell_price = row.get_cell_for('price')
        assert cell_price.exists()
        assert cell_price.text == "7.99", cell_price.text

    def test_list_table_cell_content(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        table = self.Browser.change_list_page.content.result_table

        # Check content of a specific cell (first row, title)
        # Assuming fixture data exists and we have at least one book
        cell_title = table.get_table_cell_for('title', 0)
        assert cell_title.text == "A Christmas Carol", cell_title.text

        cell_author = table.get_table_cell_for('author', 0)
        assert cell_author.text == "Dickens, Charles", cell_author.text

    def test_list_table_cell_isbn(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        table = self.Browser.change_list_page.content.result_table

        cell_isbn = table.get_table_cell_for('isbn', 0)
        assert cell_isbn.exists()
        assert cell_isbn.text == "9780141389479", cell_isbn.text

    def test_list_table_cell_price(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        table = self.Browser.change_list_page.content.result_table

        cell_price = table.get_table_cell_for('price', 0)
        assert cell_price.exists()
        assert cell_price.text == "7.99", cell_price.text

    def test_list_table_all_visible_columns_for_title(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        table = self.Browser.change_list_page.content.result_table

        title_cells = table.get_all_visible_columns_for('title')
        assert len(title_cells) == 99, f"Expected exactly 99 visible title column cell (is {len(title_cells)})"
        for cell in title_cells:
            assert len(cell.text) > 0

    # --- Filters ---

    def test_list_filter_sidebar_exists(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        filter_sidebar = self.Browser.change_list_page.content.filter_sidebar
        assert filter_sidebar.exists()
        assert filter_sidebar.h2_title.text == "FILTER"



    def test_list_filters_present(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        filter_sidebar = self.Browser.change_list_page.content.filter_sidebar

        filters = filter_sidebar.get_filters()
        # Based on BookAdmin: list_filter = ['categories', 'author', 'publication_date']
        # Django also adds 'By ...' titles to filters
        filter_titles = [f.h3_title.text for f in filters]
        assert filter_titles == ['By categories', 'By author', 'By publication date'], filter_titles

    def test_list_filter_choices(self):
        self.Browser.change_list_page.open(app='book', model='book')
        self.Browser.change_list_page.wait_for_page()
        filter_sidebar = self.Browser.change_list_page.content.filter_sidebar

        filters = filter_sidebar.get_filters()
        # Find the 'By author' filter
        category_filter = filters[0]
        author_filter = filters[1]
        pub_date_filter = filters[2]

        assert category_filter.h3_title.text == "By categories"
        assert author_filter.h3_title.text == "By author"
        assert pub_date_filter.h3_title.text == "By publication date"

        def check_filter(filter_to_check, expected_choices):
            choices = filter_to_check.get_choices()
            assert len(choices) == len(expected_choices), len(choices)
            choice_texts = [c.text for c in choices]
            assert choice_texts == expected_choices, choice_texts
            # make sure that elements really exist
            for choice in choices:
                assert choice.exists()

        check_filter(
            category_filter,
            ['All', 'Adventure', "Children's Literature", 'Classic Literature', 'Comedy', 'Drama',
             'Epic', 'Fantasy', 'Fiction', 'Gothic Fiction', 'Historical Fiction', 'Horror', 'Mystery', 'Philosophy',
             'Poetry', 'Romance', 'Satire', 'Science Fiction', 'Social Commentary', 'Thriller', 'Tragedy', '-']
        )

        check_filter(
            author_filter,
            ['All', 'Alcott, Louisa May', 'Alighieri, Dante', 'Austen, Jane',
             'Balzac, Honoré de', 'Baum, L. Frank', 'Brontë, Charlotte', 'Brontë, Emily', 'Carroll, Lewis',
             'Cervantes, Miguel de', 'Chekhov, Anton', 'Conrad, Joseph', 'Defoe, Daniel', 'Dickens, Charles',
             'Dostoevsky, Fyodor', 'Doyle, Arthur Conan', 'Dumas, Alexandre', 'Eliot, George', 'Flaubert, Gustave',
             'Hardy, Thomas', 'Hawthorne, Nathaniel', 'Hugo, Victor', 'James, Henry', 'Joyce, James', 'Kafka, Franz',
             'Kipling, Rudyard', 'London, Jack', 'Melville, Herman', 'Poe, Edgar Allan', 'Shakespeare, William',
             'Shelley, Mary', 'Stevenson, Robert Louis', 'Stoker, Bram', 'Swift, Jonathan', 'The Greek, Homer',
             'Tolstoy, Leo', 'Twain, Mark', 'Verne, Jules', 'Wells, H.G.', 'Wilde, Oscar', 'Zola, Émile', '-']
        )

        check_filter(
            pub_date_filter,
            ['Any date', 'Today', 'Past 7 days', 'This month', 'This year', 'No date', 'Has date']
        )
