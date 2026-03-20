from playwright.sync_api import Locator, Page

from config import settings


class WikipediaPage:
    def __init__(self, page: Page, config: settings.WikipediaConfig = settings.WikipediaConfig()):
        self.page: Page = page
        self.config: settings.WikipediaConfig = config
        self.search_input: Locator = page.locator('#searchInput')
        self.english_link: Locator = page.get_by_role('link', name=self.config.english_link_text)
        self.talk_link: Locator = page.get_by_role('link', name=self.config.talk_link_text)
        self.view_source_link: Locator = page.locator('#ca-viewsource')

    def navigate(self):
        self.page.goto(self.config.main_page_url)

    def open_portal_page(self):
        self.page.goto(self.config.portal_url)

    def open_english_main_page(self):
        self.open_portal_page()
        self.english_link.click()

    def search(self, text: str):
        self.search_input.fill(text)
        self.search_input.press('Enter')

    def open_talk_page(self):
        self.talk_link.click()

    def open_view_source(self):
        self.view_source_link.click()
