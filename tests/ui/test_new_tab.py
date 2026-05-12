from playwright.sync_api import Page, expect


def test_new_tab(page: Page):
    page.goto('https://www.qa-practice.com/elements/new_tab/link')
    with page.expect_popup() as new_tab_event:
        page.locator('#new-page-link').click()
    new_tab = new_tab_event.value
    new_tab.wait_for_load_state()
    expect(new_tab.locator('#result-text')).to_have_text('I am a new page in a new tab')
    expect(new_tab.locator('#req_header')).to_be_visible()
