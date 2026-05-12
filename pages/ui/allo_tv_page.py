from playwright.sync_api import Page, Locator


class AlloTVPage:
    def __init__(self, page: Page):
        self.page = page
        self.promo_close_btn: Locator = page.locator('button.close[aria-label="Close"]')
        self.sort_toggle: Locator = page.locator('.a-select__toggle')
        self.sort_by_name_option: Locator = page.locator('li.base-drop__item').filter(has_text='за назвою')

    def navigate(self):
        self.page.goto('https://allo.ua/ua/televizory/proizvoditel-xiaomi/')

    def close_promo_if_visible(self):
        if self.promo_close_btn.is_visible():
            self.promo_close_btn.click()

    def sort_by_name(self):
        self.sort_toggle.click()
        self.sort_by_name_option.click()
