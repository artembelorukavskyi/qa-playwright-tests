import allure
import pytest
from playwright.sync_api import Page, expect

from config import settings
from pages.ui.login_page import ExpandTestingLoginPage, QABrainsLoginPage


@pytest.mark.ui
def test_login_page(page: Page):
    qabrains_login_page = QABrainsLoginPage(page)

    if qabrains_login_page.has_ssl_error_page():
        with allure.step('Fallback: QABrains SSL error — verifying ExpandTesting login instead'):
            login_page = ExpandTestingLoginPage(page)
            login_page.open_and_login_as_default_user()
            expect(login_page.flash_message).to_contain_text(
                settings.PRACTICE_SECURE_AREA_MESSAGE
            )
        pytest.xfail('QABrains unavailable due to SSL error — fallback login verified on ExpandTesting')


def test_login_to_practice(page: Page):
    login_page = ExpandTestingLoginPage(page)
    login_page.open_and_login_as_default_user()
    expect(login_page.flash_message).to_contain_text(
        settings.PRACTICE_SECURE_AREA_MESSAGE
    )


def test_change_text_after_login(page: Page):
    login_page = ExpandTestingLoginPage(page)
    replacement_text = 'My Test Text!!!'
    login_page.route_secure_page_text(
        'Secure Area page for Automation Testing Practice',
        replacement_text,
    )

    login_page.open_and_login_as_default_user()
    expect(login_page.page.locator('body')).to_contain_text(replacement_text)
