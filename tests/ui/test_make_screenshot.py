from playwright.sync_api import Page

def test_screenshot(page: Page):
    page.goto('https://www.qa-practice.com/')
    page.screenshot(path='allure-results/screenshots/screenshots.png')
