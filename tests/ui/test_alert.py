from playwright.async_api import expect

from playwright.sync_api import Page, expect

from playwright.sync_api import Page, expect


def test_alert_on_page(page: Page):
    page.goto('https://www.qa-practice.com/elements/alert/confirm')

    page.once('dialog', lambda dialog: dialog.accept())
    page.locator('a.a-button').click()

    expect(page.locator('#result-text')).to_have_text('Ok')
