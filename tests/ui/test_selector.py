from playwright.sync_api import Page, expect


def test_selector(page: Page):
    page.goto('https://www.qa-practice.com/elements/select/single_select')
    page.locator('#id_choose_language').first.select_option('Python')
    expect(page.locator('#id_choose_language')).to_contain_text('Python')
