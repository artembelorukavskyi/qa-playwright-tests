from playwright.sync_api import Page, expect

from pages.ui.wikipedia_page import WikipediaPage


def test_wikipedia_about(page: Page):
    wikipedia_page = WikipediaPage(page)
    wikipedia_page.open_english_main_page()
    expect(page.get_by_text('Welcome to Wikipedia,')).to_be_visible()
    expect(page).to_have_title('Wikipedia, the free encyclopedia')


def test_wiki_talk_page(page: Page):
    wikipedia_page = WikipediaPage(page)
    wikipedia_page.open_english_main_page()
    wikipedia_page.open_talk_page()
    wikipedia_page.open_view_source()
    expect(page.get_by_role('heading', name='Talk:Main Page')).to_be_visible()
    expect(page.get_by_role('heading', name='View source for Talk:Main Page')).to_be_visible()
    expect(page.locator('#mw-content-text')).to_contain_text(
        'You do not have permission to edit this page'
    )


def test_wikipedia_search(page: Page):
    wikipedia_page = WikipediaPage(page)
    wikipedia_page.navigate()
    wikipedia_page.search('Playwright')
    expect(page.locator('#firstHeading')).to_have_text('Playwright')
    expect(page).to_have_title('Playwright - Wikipedia')
